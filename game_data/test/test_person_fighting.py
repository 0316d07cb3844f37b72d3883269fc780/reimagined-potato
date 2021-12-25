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
        self.assertTrue(len(my_Person.drawpile)==5)

    def test_drawing_cards(self):
        my_person = make_person()
        self.assertEqual(len(my_person.drawpile),5)
        my_card=my_person.drawpile.get_a_card()
        my_card.move(my_person.discardpile)
        for _ in range(4):
            my_person.draw_Card()
        self.assertEqual(len(my_person.drawpile),0)
        self.assertEqual(len(my_person.discardpile),1)
        self.assertEqual(len(my_person.hand),4)
        my_person.draw_Card()
        self.assertEqual(len(my_person.drawpile),0)
        self.assertEqual(len(my_person.discardpile),0)
        self.assertEqual(len(my_person.hand),5)



if __name__ == '__main__':
    unittest.main()

def make_person():
    return Person(make_person_data())
