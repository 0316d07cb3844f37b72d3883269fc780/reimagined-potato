"""
Contains the underlying data of a Card inside a scene.
"""

from game_data.src.getter_scene import getter
from game_data.src.action_factory import Action_Factories, create_from_string
from utility.src.string_utils import create_tag, detag_given_tags


class Card:
    def __init__(self, name, action_factory, speed, target_checker, location):
        self.name = name
        self.action_factory = action_factory
        self.speed = speed
        self.target_checker = target_checker
        getter.register(self)
        self.location = location
        location.add_card(self)

    def move(self, new_location):
        self.location.remove_card(self)
        new_location.add_card(self)

    def resolve(self, player, target_list):
        if not self.target_checker(target_list):
            raise IndexError
        self.action_factory(player, target_list)

    def __str__(self):
        my_string = create_tag("name", self.name)
        my_string += create_tag("action_factory", str(self.action_factory))
        my_string += create_tag("speed", str(self.speed))
        my_string += create_tag("target_checker", str(self.target_checker))
        my_string += create_tag("location", self.location.scene_id)
        return my_string

    @classmethod
    def create_from_string(cls, string):
        name, action_factory, speed, target_checker, location = detag_given_tags(string, "name", "action_factory", "speed", "target_checker", "location")
        action_factory = create_from_string(action_factory)
        speed = getattr(Speed, speed)
        target_checker = getattr(Target_Checker, target_checker)
        location = getter[int(location)]
        return Card(name, action_factory, speed, target_checker, location)

    def __eq__(self, other):
        return str(self) == str(other)


from enum import Enum


class Speed(Enum):
    Channel = 0
    Regular = 1
    Fast = 2
    Instant = 3

    def __str__(self):
        return self.name


class Target_Checker(Enum):
    no_target = lambda targetlist: len(targetlist) == 0, "no_target"
    single_target = lambda targetlist: len(targetlist) == 1, "single_target"

    def __str__(self):
        return self.name

    def __call__(self, target_list):
        return self.value[0](target_list)


def create_card(cardname, location):
    return cards_by_string[cardname](location)


def create_tackle(location):
    tackle = Card("Tackle", Action_Factories.tackle_factory, Speed.Fast, Target_Checker.single_target, location)
    return tackle


def create_brace(location):
    brace = Card("Brace", Action_Factories.brace_factory, Speed.Instant, Target_Checker.no_target, location)
    return brace


cards_by_string = {
    "Tackle": create_tackle,
    "Brace": create_brace
}
