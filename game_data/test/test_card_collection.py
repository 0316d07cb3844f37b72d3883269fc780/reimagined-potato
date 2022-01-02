import unittest

from game_data.src.card import create_tackle
from game_data.src.card_collection import Card_Collection


class MyTestCard_Collection(unittest.TestCase):
    def test_in(self):
        my_collection = Card_Collection([])
        my_card = create_tackle(my_collection)
        self.assertTrue(my_card in my_collection)


if __name__ == '__main__':
    unittest.main()
