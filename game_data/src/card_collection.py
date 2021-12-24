"""
Contains a collection of cards. Meant to be derived from.
"""

class card_collection():
    def __init__(self,cardlist):
        self.cards={}
        for card in cardlist:
            self.cards[card.ID] = card


    def __len__(self):
        return len(self.cards)
