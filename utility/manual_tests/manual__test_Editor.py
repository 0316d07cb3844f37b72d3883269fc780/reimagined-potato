import unittest
from utility.src.Editor import *
import tkinter


class MyTestCase(unittest.TestCase):
    def test_something(self):
        make_test_frame()


if __name__ == '__main__':
    unittest.main()


def make_test_frame():
    root = tkinter.Tk()
    root.mainloop()
