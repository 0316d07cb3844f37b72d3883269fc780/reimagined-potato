import unittest

from game_data.src.person_fighting import Person_Fighting
from game_data.src.action import create_tackle
from game_io.src.action_io import ActionIO
from game_io.manual_tests.base_test import test_sprite


class MyTestCase(unittest.TestCase):
    def test_something(self):
        tackler = Person_Fighting.create_from_string("<file>resources\\People\\Fighting\\dog.person_fighting<\\file>")
        tacklee = Person_Fighting.create_from_string("<file>resources\\People\\Fighting\\knight.person_fighting<\\file>")
        tackle = create_tackle(tackler, [tacklee])
        test_sprite(lambda : ActionIO(tackle))



if __name__ == '__main__':
    unittest.main()
