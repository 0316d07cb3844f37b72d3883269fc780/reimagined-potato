"""
A person as it is in the Fight_Scene.
"""

from game_data.src.card_collection import Card_Collection, create_drawpile
from game_data.src.getter_scene import getter


class Person_Fighting():
    def __init__(self, base_person):
        self.person = base_person
        self.actions = []
        self.resist = 0
        "Create Cardcontainers."
        self.drawpile = create_drawpile(base_person.deck)
        self.hand = Card_Collection([])
        self.discardpile = Card_Collection([])
        "Register in universal getter."
        self.scene_id = getter.register(self)

    def damage(self, damage):
        if damage > self.resist:
            self.person.damage(damage - self.resist)
            self.resist = 0
        else:
            self.resist -= damage

    def play_Card(self, card, target_list):
        """
        Plays a card from hand.
        :param card: The card to be played.
        :param target_list: Possibly empty list of targets.
        :return:
        """
        if card not in self.hand:
            raise IndexError("Card not in Hand can't be played.")
        card.resolve(self, target_list)
        card.move(self.discardpile)

    def draw_Card(self):
        if len(self.drawpile) != 0:
            card = self.drawpile.get_a_card()
            card.move(self.hand)
        elif len(self.discardpile) != 0:
            self.shuffle_discardpile_into_drawpile()
            self.draw_Card()

    def shuffle_discardpile_into_drawpile(self):
        for card in self.discardpile.get_all_cards():
            card.move(self.drawpile)
        self.drawpile.shuffle()

    def get_health(self):
        return self.person.health

    def append_action(self, action):
        self.actions.append(action)

    def die(self):
        pass


def get_Person(id):
    return Person_Fighting.all_people[id]
