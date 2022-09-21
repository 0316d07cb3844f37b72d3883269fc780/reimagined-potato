import unittest
from game_data.src.persondata import PersonData as Person


class Test_Testtype_Person(unittest.TestCase):
    def test_damage(self):
        my_person = make_person()
        my_person.damage(3)
        self.assertEqual(my_person.health,7,"Damage calculation error.")

    def test_to_and_from_string(self):
        my_person=make_person()
        my_person.damage(2)
        person_string=str(my_person)
        remade= Person.create_from_string(person_string)
        self.assertEqual(remade.health,my_person.health)
        self.assertEqual(remade.deck, my_person.deck)




if __name__ == '__main__':
    unittest.main()

def make_person():
    my_person = Person(10, "Testtype", deck=["Tackle"]*5+["Brace"]*5)
    return my_person