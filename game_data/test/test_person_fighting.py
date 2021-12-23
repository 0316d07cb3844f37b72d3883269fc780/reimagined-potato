import unittest
from test_person_data import make_person as make_person_data
from game_data.src.person_fighting import Person_Fighting as Person

class Test_Person_Fighting(unittest.TestCase):
    def test_damage(self):
        my_Person = make_person()
        health_before = my_Person.get_health()
        my_Person.damage(4)
        health_after = my_Person.get_health()
        self.assertEqual(health_before-4,health_after)


if __name__ == '__main__':
    unittest.main()

def make_person():
    return Person(make_person_data())
