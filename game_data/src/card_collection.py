"""
Contains a collection of cards. Meant to be derived from.
"""

import random

from game_data.src.loadable import Loadable
from game_data.src.card import create_card, Card
from game_data.src.getterscene import getter
from utility.src.string_utils import create_tag, detag_given_tags, detag_repeated, root_path


class Card_Collection(Loadable):
    def __init__(self, card_list: list):
        self.cards = {}
        self.scene_id = getter.register(self)
        for card in card_list:
            self.cards[card.scene_id] = card
            card.location=self
        self.card_order = [card.scene_id for card in card_list]


    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards.values())

    def __contains__(self, card):
        return card in self.cards.values()

    def __str__(self) -> str:
        cards_string = "\n".join([create_tag("card", card) for card in self.get_all_cards()])
        result = create_tag("cards", cards_string) + "\n"
        result += create_tag("scene_id", self.scene_id)
        return result

    @classmethod
    def create_from_string(cls, string: str):
        possible_filename = detag_given_tags("file")
        if len(possible_filename) == 1:
            with open(root_path(*possible_filename)) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        cards_string, scene_id = detag_given_tags(string, "cards", "scene_id")
        card_strings = detag_repeated(cards_string, "card")
        card_list = [Card.create_from_string(my_string) for my_string in card_strings]
        result = Card_Collection(card_list)
        if scene_id != "":
            scene_id = int(scene_id)
            getter[scene_id] = result
        return result

    def get_a_card(self) -> Card:
        if len(self) == 0:
            raise IndexError("Card_Container empty")
        card_id = self.card_order[-1]
        return self.cards[card_id]

    def get_all_cards(self) -> list:

        return [self.cards[card_id] for card_id in self.card_order]

    def remove_card(self, card: Card) -> None:
        """
        Use card.move instead if possible.
        :param card: the card to remove.
        :return:
        """
        if card in self:
            self.card_order.remove(card.scene_id)
            self.cards.pop(card.scene_id)
            card.location = None

    def add_card(self, card: Card):
        """
        Use card.move instead if possible.
        :param card: card to add.
        :return:
        """
        if not card.scene_id in self.card_order:
            self.card_order.append(card.scene_id)
        self.cards[card.scene_id] = card
        card.location = self

    def shuffle(self):
        random.shuffle(self.card_order)


def create_drawpile(deck: list) -> Card_Collection:
    drawpile = Card_Collection([])
    for card in deck:
        create_card(card, drawpile)
    return drawpile
