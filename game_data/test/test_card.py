import unittest
from game_data.src.card import create_tackle, TargetChecker, Card
from game_data.src.card_collection import Card_Collection


class CardCase(unittest.TestCase):
    def test_stringing(self):
        my_Collection = Card_Collection([])
        my_card = create_tackle(my_Collection)
        my_card_from_string = Card.create_from_string(str(my_card))
        self.assertEqual(my_card, my_card_from_string)

    def test_target_checker(self):
        pass


if __name__ == '__main__':
    unittest.main()
