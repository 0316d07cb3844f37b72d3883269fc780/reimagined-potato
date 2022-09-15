import unittest
from utility.src.Editor import *
import tkinter


class MyTestCase(unittest.TestCase):
    def test_int_attribute_frame(self):
        root = make_test_frame()
        IntAttributeWidget(root, "test", "3")
        root.mainloop()

    def test_file_attribute_frame(self):
        root = make_test_frame()
        FileAttributeWidget(root, "test", "card.card")
        root.mainloop()


if __name__ == '__main__':
    unittest.main()


def make_test_frame():
    root = tkinter.Tk()
    return root
