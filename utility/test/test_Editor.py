import unittest
from utility.src.Editor import *
import tkinter

class MyTestCase(unittest.TestCase):

    def test_string_attribute_widget(self):
        root = tkinter.Tk()
        widget = StringAttributeWidget(root, "test", "test_value")
        print(widget.value_as_tags())


if __name__ == '__main__':
    unittest.main()

