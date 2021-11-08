import unittest
from game_data.src.person_data import Person_Data as Person


class MyTestCase(unittest.TestCase):
    def test_something(self):
        my_person=Person(10, "Testtype")
        my_person.damage(3)
        self.assertEqual(my_person.health,7,"Damage calculation error.")






if __name__ == '__main__':
    unittest.main()
