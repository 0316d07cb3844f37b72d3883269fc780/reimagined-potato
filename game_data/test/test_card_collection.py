import unittest

from game_data.src.card import create_tackle
from game_data.src.card_collection import Card_Collection, create_drawpile


class MyTestCard_Collection(unittest.TestCase):
    def test_in(self):
        my_collection = Card_Collection([])
        my_card = create_tackle(my_collection)
        self.assertTrue(my_card in my_collection)

    def test_to_string(self):
        my_collection=create_drawpile(["Tackle"]*5+["Brace"]*3)
        my_new_collection=Card_Collection.create_from_string(str(my_collection))
        for card in my_collection:
            self.assertTrue(card in my_new_collection)



if __name__ == '__main__':
    unittest.main()
