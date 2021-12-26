import unittest
from game_data.src.person_data import Person_Data as Person


class Test_Testtype_Person(unittest.TestCase):
    def test_damage(self):
        my_person = make_person()
        my_person.damage(3)
        self.assertEqual(my_person.health,7,"Damage calculation error.")




if __name__ == '__main__':
    unittest.main()

def make_person():
    my_person = Person(10, "Testtype", deck=["Tackle"]*5+["Brace"]*5)
    return my_person