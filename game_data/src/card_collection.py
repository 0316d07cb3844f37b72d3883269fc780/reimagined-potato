"""
Contains a collection of cards. Meant to be derived from.
"""

from game_data.src.card import create_card, Card
from game_data.src.getter_scene import getter
from utility.src.string_utils import create_tag, detag_given_tags, detag_repeated


class Card_Collection():
    def __init__(self, cardlist: list):
        self.cards = {}
        for card in cardlist:
            self.cards[card.scene_id] = card
        self.scene_id = getter.register(self)

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards.values())

    def __contains__(self, card):
        return card in self.cards.values()

    def __str__(self) -> str:
        def string_card_pair(id, card):
            result = create_tag("id", str(id)) + create_tag("card", str(card))
            return create_tag("card_pair", result)

        cards_string = str(",".join(["\n" + string_card_pair(id, card) for id, card in self.cards.items()]))
        result = create_tag("cards", cards_string + "\n") + "\n"
        result += create_tag("scene_id", self.scene_id)
        return result

    @classmethod
    def create_from_string(cls, string: str):
        possible_filename = detag_given_tags("file")
        if len(possible_filename) == 1:
            with open(*possible_filename) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        cards_tagged_string, scene_id_string = detag_given_tags(string, "cards", "scene_id")
        cards_tagged_list = detag_repeated(cards_tagged_string, "card_pair")
        card_pairs_string = [detag_given_tags(card_pair, "id", "card") for card_pair in cards_tagged_list]
        card_pairs = [(int(id), Card.create_from_string(card + create_tag("location", scene_id_string))) for id, card in
                      card_pairs_string]
        my_collection = Card_Collection([])
        for id, card in card_pairs:
            my_collection.cards[id] = card
        getter[int(scene_id_string)] = my_collection
        return my_collection

    def get_a_card(self) -> Card:
        if len(self) == 0:
            raise IndexError("Card_Container empty")
        values = iter(self.cards.values())
        return next(values)

    def get_all_cards(self) -> list:
        return list(self.cards.values())

    def remove_card(self, card: Card) -> None:
        """
        Use card.move instead if possible.
        :param card: the card to remove.
        :return:
        """
        self.cards.pop(card.scene_id)
        card.location = None

    def add_card(self, card: Card):
        """
        Use card.move instead if possible.
        :param card: card to add.
        :return:
        """
        self.cards[card.scene_id] = card
        card.location = self

    def shuffle(self):
        pass


def create_drawpile(deck: list) -> Card_Collection:
    drawpile = Card_Collection([])
    for card in deck:
        create_card(card, drawpile)
    return drawpile
