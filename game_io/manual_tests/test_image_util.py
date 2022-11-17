import unittest
from base_test import test_surface
from game_io.src.image_util import *


class MyTestCase(unittest.TestCase):
    def test_make_text_field(self):
        text = "First Line\nNew Line"
        make_text = lambda: make_text_field(text, size=12)
        test_surface(make_text)

    def test_make_image(self):
        make_test_image= lambda : make_image("resources/Testguy.bmp")
        test_surface(make_test_image)


if __name__ == '__main__':
    unittest.main()
