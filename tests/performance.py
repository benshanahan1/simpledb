import shutil
import os
import time
import uuid
from simpledb import SimpleDb


def test_engine_performance():
    # TODO: convert this to test fixture!
    shutil.rmtree("tests/data")
    os.makedirs("tests/data", exist_ok=True)
    db = SimpleDb("tests/data/integration-test-2.db")

    n_iters = 2_500
    set_times = []
    get_times = []

    print(f"running {n_iters} iterations...")

    for _ in range(n_iters):
        expected_key = uuid.uuid4().bytes
        expected_value = uuid.uuid4().bytes

        start_time_set = time.time()
        db.set(expected_key, expected_value)
        set_times.append(time.time() - start_time_set)

        start_time_get = time.time()
        key, value = db.get(expected_key)
        get_times.append(time.time() - start_time_get)

        assert key == expected_key
        assert value == expected_value

    print("average set: {:.2f} ms".format(1000 * sum(set_times) / float(n_iters)))
    print("average get: {:.2f} ms".format(1000 * sum(get_times) / float(n_iters)))


if __name__ == "__main__":
    test_engine_performance()
