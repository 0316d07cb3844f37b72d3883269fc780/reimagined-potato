"""
Contains the Person class representing characters as game units. Contains attributes that persist between fights.
"""

from game_data.src.getter_scene import getter
from utility.src.string_utils import create_tag, detag_given_tags, detag_repeated


class Person_Data:
    legal_types = ["Testtype"]

    def __init__(self, max_health: int, type: str, deck: list = []):
        self.max_health = self.health = max_health
        self.deck = deck
        self.scene_id = getter.register(self)

        if (type in Person_Data.legal_types):
            self.person_type = type
        else:
            raise Exception("Illegal type")

    def __str__(self):
        my_string = create_tag("max_health", self.max_health) + create_tag("health", self.health)
        deck_string = ""
        for card in self.deck:
            deck_string += "\n" + create_tag("card", card)
        my_string += create_tag("deck", deck_string)
        my_string += create_tag("scene_id", self.scene_id)
        my_string += create_tag("person_type", self.person_type)
        return my_string

    @classmethod
    def create_from_string(cls, string: str):
        filename,=detag_given_tags("file")
        if filename!="":
            with open(filename) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        max_health, health, scene_id, person_type = detag_given_tags(string, "max_health", "health", "scene_id",
                                                                     "person_type")
        deck_string, = detag_given_tags(string, "deck")
        deck = detag_repeated(deck_string, "card")
        my_person = Person_Data(int(max_health), person_type, deck)
        my_person.health = int(health)
        getter[scene_id] = my_person
        return my_person

    def damage(self, damage: int):
        self.health -= damage
        if (self.health <= 0):
            self.die()

    def die(self):
        pass
