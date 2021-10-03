# simpledb

Simple pure-Python LSM key-value storage engine.

## usage
Install package via Pip.
```bash
pip install git+https://github.com/benshanahan1/simpledb
```

Usage:
```python
>>> from simpledb import SimpleDb
>>> db = SimpleDb("path/to/my.db")
>>> db.set(b"foo", b"bar")
>>> db.set(b"bar", b"baz")
>>> db.get(b"foo")
b'bar'
>>> db.keys
[b'foo', b'bar']
```

## development
```bash
pip install -e .[dev]
```

### test
```bash
pytest
```

Run performance test:
```bash
python tests/performance.py
```
