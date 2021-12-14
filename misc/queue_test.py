import unittest
from queue import Queue


def target(*args, **kwargs):
    return (args, kwargs)


class TestQueue(unittest.TestCase):

    def test_append(self):
        q = Queue(10)
        self.assertEqual(0, len(q))
        for i in range(10):
            q.append(i)
        self.assertEqual(10, len(q))

    def test_overflow(self):
        q = Queue(10)
        for i in range(11):
            q.append(i)
        self.assertEqual(10, len(q))
        print("q.items:" + str(q.items))
        self.assertTupleEqual(tuple(range(10, 0, -1)), tuple(q))


if __name__ == '__main__':
    unittest.main()
