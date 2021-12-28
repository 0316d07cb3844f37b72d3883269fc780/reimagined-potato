import unittest
from test_person_data import make_person as make_person_data
from game_data.src.person_fighting import Person_Fighting as Person
from game_data.src.card import create_tackle

class Test_Person_Fighting(unittest.TestCase):
    def test_damage(self):
        my_Person = make_person()
        health_before = my_Person.get_health()
        my_Person.damage(4)
        health_after = my_Person.get_health()
        self.assertEqual(health_before-4,health_after)
        self.assertTrue(len(my_Person.drawpile)==10)

    def test_drawing_cards(self):
        my_person = make_person()
        self.assertEqual(len(my_person.drawpile),10)
        my_card=my_person.drawpile.get_a_card()
        my_card.move(my_person.discardpile)
        for _ in range(9):
            my_person.draw_Card()
        self.assertEqual(len(my_person.drawpile),0)
        self.assertEqual(len(my_person.discardpile),1)
        self.assertEqual(len(my_person.hand),9)
        my_person.draw_Card()
        self.assertEqual(len(my_person.drawpile),0)
        self.assertEqual(len(my_person.discardpile),0)
        self.assertEqual(len(my_person.hand),10)

    def test_playing_card(self):
        tackler, tackled =make_person(),make_person()
        create_tackle(tackler.hand)
        my_tackle=tackler.hand.get_a_card()
        tackler.play_Card(my_tackle,[tackled])
        self.assertEqual(len(tackler.actions),1)

    def test_getting_person_by_id(self):
        my_person, another_person=make_person(),make_person()
        self.assertEqual((my_person,another_person),(Person.all_people[my_person.id],Person.all_people[another_person.id]))
        self.assertTrue(not Person.all_people[my_person.id]==Person.all_people[another_person.id])




if __name__ == '__main__':
    unittest.main()

def make_person():
    return Person(make_person_data())
