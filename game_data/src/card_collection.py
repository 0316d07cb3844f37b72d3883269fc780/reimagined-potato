"""
Contains a collection of cards. Meant to be derived from.
"""

from game_data.src.card import create_card

class Card_Collection():
    def __init__(self,cardlist, person):
        self.cards={}
        for card in cardlist:
            self.cards[card.ID] = card
        self.person=person


    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards.values())

    def get_a_card(self):
        if len(self)==0:
            raise IndexError("Card_Container empty")
        values=iter(self.cards.values())
        return next(values)

    def get_all_cards(self):
        return list(self.cards.values())


    def remove_card(self, card):
        """
        Use card.move instead if possible.
        :param card: the card to remove.
        :return:
        """
        self.cards.pop(card.ID)
        card.location = None

    def add_card(self, card):
        """
        Use card.move instead if possible.
        :param card: card to add.
        :return:
        """
        self.cards[card.ID]=card
        card.location=self

    def shuffle(self):
        pass

def create_drawpile(deck, person):
    drawpile = Card_Collection([], person)
    cardlist=[create_card(card,drawpile) for card in deck]
    for card in cardlist:
        drawpile.add_card(card)
    return drawpile

