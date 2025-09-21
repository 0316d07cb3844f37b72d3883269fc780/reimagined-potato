"""
Contains the Person class representing characters as game units. Contains attributes that persist between fights.
"""

from game_data.src.loadable import Loadable
from game_data.src.getterscene import getter
from utility.src.string_utils import create_tag, detag_given_tags, detag_repeated, read_and_clean_file


class PersonData(Loadable):
    legal_types = ["Testtype", "Knight", "Dog"]

    def __init__(self, max_health: int, person_type: str, deck: list = None):
        self.max_health = self.health = max_health
        if deck is None:
            self.deck = []
        else:
            self.deck = deck
        self.scene_id = getter.register(self)

        if person_type in PersonData.legal_types:
            self.person_type = person_type
        else:
            raise Exception("Illegal person_type")

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
        possible_filename, = detag_given_tags(string, "file")
        if possible_filename != "":
            file_contents = read_and_clean_file(possible_filename)
            return cls.create_from_string(file_contents)
        max_health, health, scene_id, person_type = detag_given_tags(string, "max_health", "health", "scene_id",
                                                                     "person_type")
        deck_string, = detag_given_tags(string, "deck")
        deck = detag_repeated(deck_string, "card")
        my_person = PersonData(int(max_health), person_type, deck)
        my_person.health = int(health)
        if scene_id != "" and scene_id != "auto":
            scene_id = int(scene_id)
        getter[scene_id] = my_person
        return my_person

    def damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        pass
