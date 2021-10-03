import struct


class Pack(object):
    """Pack key-value pair into a byte array.

    The byte array is constructed as follows:
        1. Unsigned int: length of the entire byte array
        2. Unsigned int: length of the key char array
        3. Char array: Char array containing the key, length specified in #2
        4. Unsigned int: length of the value char array
        5. Char array: Char array containing the value, length specified in #4
    """

    PAIRSIZE_T = "I"
    PAIRSIZE_S = struct.calcsize(PAIRSIZE_T)
    KVSIZE_T = "I"
    KVSIZE_S = struct.calcsize(KVSIZE_T)
    CONTENT_T = "{}s"

    def pack(self, key, value):
        """Pack a key-value pair into a byte array.

        :param bytes key: Key, in bytes.
        :param bytes value: Value, in bytes.
        """
        assert isinstance(key, bytes), "Key must be of type `bytes`."
        assert isinstance(value, bytes), "Value must be of type `bytes`."

        key_len = len(key)
        value_len = len(value)
        total_len = self.PAIRSIZE_S + 2 * self.KVSIZE_S + key_len + value_len

        key_content_t = self.CONTENT_T.format(key_len)
        value_content_t = self.CONTENT_T.format(value_len)

        fmt = f"<{self.PAIRSIZE_T}{self.KVSIZE_T}{key_content_t}{self.KVSIZE_T}{value_content_t}"

        return struct.pack(fmt, total_len, key_len, key, value_len, value)

    def unpack(self, packed_bytes):
        """Unpack a key-value pair from a packed byte array."""
        offset = 0

        # Read the total length and assert that the total length matches the received bytes.
        total_len = struct.unpack_from(self.PAIRSIZE_T, packed_bytes, offset)[0]
        assert total_len == len(packed_bytes), "Byte array size mismatch."
        offset += self.PAIRSIZE_S

        # Unpack key length and then use that to unpack the key itself.
        key_len = struct.unpack_from(self.KVSIZE_T, packed_bytes, offset)[0]
        offset += self.KVSIZE_S

        fmt = self.CONTENT_T.format(key_len)
        key = struct.unpack_from(fmt, packed_bytes, offset)[0]
        offset += struct.calcsize(fmt)

        # Unpack value length and then use that to unpack the value itself.
        value_len = struct.unpack_from(self.KVSIZE_T, packed_bytes, offset)[0]
        offset += self.KVSIZE_S

        fmt = self.CONTENT_T.format(value_len)
        value = struct.unpack_from(fmt, packed_bytes, offset)[0]

        return (key, value)

    def unpack_pair_size(self, packed_bytes):
        """Unpack only the size of the packed key-value pair."""
        return struct.unpack_from(self.PAIRSIZE_T, packed_bytes, 0)[0]
