import unittest
from game_data.src.action_factory import create_from_string, Factories


class MyTestCase(unittest.TestCase):
    def test_create_from_string(self):
        my_factory=create_from_string("Tackle_Factory")
        self.assertEqual(create_from_string(str(my_factory)),my_factory)


if __name__ == '__main__':
    unittest.main()
