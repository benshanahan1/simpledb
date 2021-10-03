from simpledb.segment import Segment


class Engine(object):
    def __init__(self, filepath="data.db"):
        self.segment = Segment(filepath)

    def get(self, key):
        return self.segment.lookup(key)

    def set(self, key, value):
        self.segment.write(key, value)

    @property
    def keys(self):
        return list(self.segment.index.keys())
