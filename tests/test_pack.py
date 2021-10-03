import json
from simpledb.pack import Pack


def test_pack_ascii_string():
    # arrange
    p = Pack()
    expected_key = b"foo"
    expected_value = b"here's a comma, and a #hashtag!"

    # act
    packed_bytestring = p.pack(expected_key, expected_value)
    key, value = p.unpack(packed_bytestring)

    # assert
    assert key == expected_key
    assert value == expected_value


def test_pack_json_string():
    # arrange
    p = Pack()
    expected_key = b"foo"
    expected_value_dict = {"1": "one", "2": "two", "three": "the third"}
    expected_value = json.dumps(expected_value_dict).encode()

    # act
    packed_bytestring = p.pack(expected_key, expected_value)
    key, value = p.unpack(packed_bytestring)

    # assert
    assert key == expected_key
    assert json.loads(value.decode()) == expected_value_dict


def test_unpack_pair_size():
    # arrange
    p = Pack()
    expected_key = b"bar"
    expected_value = b"baz"
    expected_pair_size = (
        p.PAIRSIZE_S + 2 * p.KVSIZE_S + len(expected_key) + len(expected_value)
    )

    # act
    packed_bytestring = p.pack(expected_key, expected_value)
    pair_size = p.unpack_pair_size(packed_bytestring)

    # assert
    assert pair_size == expected_pair_size
