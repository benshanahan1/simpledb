import os
import shutil
from simpledb import SimpleDb


def test_engine():
    # arrange
    # TODO: convert this to test fixture!
    shutil.rmtree("tests/data")
    os.makedirs("tests/data", exist_ok=True)
    db = SimpleDb("tests/data/integration-test-1.db")
    expected_key = b"foo"
    expected_value = b"bar"

    # act
    db.set(expected_key, expected_value)
    key, value = db.get(expected_key)

    # assert
    assert key == expected_key
    assert value == expected_value
