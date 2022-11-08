import unittest

from game_data.src.card import create_tackle
from game_data.src.getterscene import getter
from game_data.src.person_fighting import Person_Fighting as Person
from game_data.test.test_person_data import make_person as make_person_data


class Test_Person_Fighting(unittest.TestCase):
    def test_damage(self):
        my_Person = make_person()
        health_before = my_Person.get_health()
        my_Person.damage(4)
        health_after = my_Person.get_health()
        self.assertEqual(health_before - 4, health_after)
        self.assertTrue(len(my_Person.drawpile) == 10)

    def test_drawing_cards(self):
        my_person = make_person()
        self.assertEqual(len(my_person.drawpile), 10)
        my_card = my_person.drawpile.get_a_card()
        my_card.move(my_person.discardpile)
        for _ in range(9):
            my_person.draw_card()
        self.assertEqual(len(my_person.drawpile), 0)
        self.assertEqual(len(my_person.discardpile), 1)
        self.assertEqual(len(my_person.hand), 9)
        my_person.draw_card()
        self.assertEqual(len(my_person.drawpile), 0)
        self.assertEqual(len(my_person.discardpile), 0)
        self.assertEqual(len(my_person.hand), 10)

    def test_playing_card(self):
        tackler, tackled = make_person(), make_person()
        create_tackle(tackler.hand)
        my_tackle = tackler.hand.get_a_card()
        tackler.play_card(my_tackle, [tackled])
        self.assertEqual(len(tackler.actions), 1)

    def test_getting_person_by_id(self):
        my_person, another_person = make_person(), make_person()
        self.assertEqual((my_person, another_person), (getter[my_person.scene_id], getter[another_person.scene_id]))
        self.assertTrue(not getter[my_person.scene_id] == getter[another_person.scene_id])

    def test_stringing_and_destringing(self):
        my_person=make_person()
        remake=Person.create_from_string(str(my_person))
        self.assertEqual(my_person.scene_id,remake.scene_id)



if __name__ == '__main__':
    unittest.main()


def make_person():
    return Person(make_person_data())
