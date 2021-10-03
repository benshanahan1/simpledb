import os
from simpledb.pack import Pack


class Segment(object):
    def __init__(self, filepath):
        self.pack = Pack()
        self.filepath = filepath
        self.offset = 0

        # re-build index
        self.index = {}
        self.build_index()

    def build_index(self):
        if not os.path.exists(self.filepath):
            return

        file_total_size = os.path.getsize(self.filepath)
        with open(self.filepath, "rb") as fd:
            offset = 0
            while offset < file_total_size:
                pair_size, kv_pair = self._read_internal(fd, seek_offset=offset)
                key, _ = kv_pair
                self.index[key] = offset
                offset += pair_size

            self.offset = offset  # update offset for subsequent writes

    def write(self, key, value):
        packed_bytes = self.pack.pack(key, value)
        with open(self.filepath, "ab") as fd:
            self.index[key] = self.offset
            self.offset += len(packed_bytes)  # compute offset for next entry
            fd.write(packed_bytes)

    def read(self, seek_offset=0):
        """Load in a key-value pair byte array from the segment file.

        See `simpledb.pack.Pack` for details on how the bytes are arranged. Basically, the first
        unsigned int in the byte array contains the total length of the pair in bytes. This means
        that by reading this value first, we can avoid having to read the entire file into memory.
        """
        with open(self.filepath, "rb") as fd:
            _, kv_pair = self._read_internal(fd, seek_offset=seek_offset)
            return kv_pair

    def _read_internal(self, descriptor, seek_offset=0):
        descriptor.seek(seek_offset)
        pair_size = self.pack.unpack_pair_size(descriptor.read(Pack.PAIRSIZE_S))
        descriptor.seek(seek_offset)
        kv_pair = self.pack.unpack(descriptor.read(pair_size))
        return pair_size, kv_pair

    def lookup(self, key):
        if not key in self.index:
            raise Exception(f"Cannot find key: {key}")
        offset = self.index[key]
        _, value = self.read(seek_offset=offset)
        return value
