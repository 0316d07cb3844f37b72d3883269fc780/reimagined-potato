import unittest
from base_test import test_surface
from game_io.src.image_util import *


class MyTestCase(unittest.TestCase):
    def test_make_text_field(self):
        text = "First Line\nNew Line"
        make_text = lambda: make_text_field(text, size=20)
        test_surface(make_text)


if __name__ == '__main__':
    unittest.main()
