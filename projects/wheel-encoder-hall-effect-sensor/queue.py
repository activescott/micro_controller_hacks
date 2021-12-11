

class Queue:
    def __init__(self, arr: array):
        """
        arr must be a pre-initialized array: Uses same typecode values as array: https://docs.python.org/3.10/library/array.html
        """
        if arra is None or len(arr) <= 0:
            raise ValueError(
                "arr must be a pre-initialized array with a length greater than 0")
        self.maxsize = len(arr)
        self.items = arr
        # next index to put an item to
        self.index = 0
        self.len = 0

    def append(self, val):
        if self.index == self.maxsize - 1:
            # we're full so lets shift first:
            self.shift_left()
        else:
            self.len += 1
        self.items[self.index] = val
        self.index += 1

    def shift_left(self):
        for i in range(1, self.maxsize - 1):
            self.items[i - 1] = self.items[i]
        self.index = self.maxsize - 1

    def __dir__(self):
        return "Queue([{}])".format(this.items)

    def dequeue(self):
        tododododododo
