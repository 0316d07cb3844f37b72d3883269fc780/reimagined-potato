"""Contains the cards to replenish a persons hand within a fight."""

from game_data.src.card import create_card
from game_data.src.card_collection import card_collection

class Drawpile(card_collection):
    def __init__(self, deck):

        cardlist=[create_card(card) for card in deck]
        super().__init__(cardlist)

