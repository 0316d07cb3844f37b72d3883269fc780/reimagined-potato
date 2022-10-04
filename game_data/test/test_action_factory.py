import unittest
from game_data.src.action_factory import  Factories, Action_Factory


class MyTestCase(unittest.TestCase):
    def test_create_from_string(self):
        my_factory= Action_Factory.create_from_string("Tackle_Factory")
        self.assertEqual(Action_Factory.create_from_string(str(my_factory)),my_factory)


if __name__ == '__main__':
    unittest.main()
