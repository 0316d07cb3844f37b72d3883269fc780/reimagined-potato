import unittest
from game_data.src.card import Card as CardData
from game_io.src.card_io import CardIO
from base_test import test_sprite


class MyTestCase(unittest.TestCase):
    def test_draw_card_from_file(self):
        card_data = CardData.create_from_string("<file>resources\\Cards\\tackle.card<\\file>")
        card = CardIO(card_data)
        test_sprite(lambda : card)


if __name__ == '__main__':
    unittest.main()
