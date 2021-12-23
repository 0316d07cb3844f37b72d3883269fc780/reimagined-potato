"""Contains the cards to replenish a persons hand within a fight."""

import game_data.src.card as card_module

class Drawpile():
    def __init__(self, deck):

        self.cards=[card_module.__getattribute__(card) for card in deck]

    def __len__(self):
        return len(self.cards)