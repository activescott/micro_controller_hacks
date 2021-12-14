# for encoder we need a simple append-only fixed-length, FIFO queue for positive integers to track speed:
from array import array


def _zeros(count: int):
    if count < 0:
        raise ValueError("count must be bigger")
    while count > 0:
        yield 0
        count -= 1


class Queue:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.items = array("I", _zeros(max_size))
        self.len = 0
        self.left = 0
        pass

    def append(self, item: int):
        self.items[self.left] = item
        if self.len < self.max_size:
            self.len += 1

        self.left += 1
        if self.left >= self.max_size:
            self.left = 0

    def __len__(self):
        return self.len

    # https://docs.python.org/3.10/library/stdtypes.html#typeiter

    def __iter__(self):
        # TODO: detect container change during iteration and raise
        start = self.left - 1
        if start < 0:
            start = self.len - 1
        yielded = 0
        while yielded < self.len:
            yield self.items[start]
            yielded += 1
            start -= 1
            if start < 0:
                start = self.max_size - 1
