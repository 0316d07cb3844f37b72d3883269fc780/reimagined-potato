"""
Contains the underlying data of a Card inside a scene.
"""

from enum import Enum

from game_data.src.loadable import Loadable
from game_data.src.action import Speed
from game_data.src.action_factory import Action_Factories, Action_Factory
from game_data.src.getter_scene import getter
from utility.src.string_utils import create_tag, detag_given_tags, root_path


class TargetChecker(Enum):
    no_target = lambda targetlist: len(targetlist) == 0, "no_target"
    single_target_non_card = lambda targetlist: len(targetlist) == 1, "single_target_non_card"
    single_target_person = lambda targetlist: len(targetlist) == 1, "single_target_person"
    single_target_action_or_stance = lambda targetlist: len(targetlist) == 1, "single_target_action_or_stance"

    def __str__(self):
        return self.name

    def __call__(self, target_list):
        return self.value[0](target_list)


class Card(Loadable):
    def __init__(self, card_type: str, name: str, action_factory: Action_Factory, speed: Speed,
                 target_checker: TargetChecker,
                 location):
        self.card_type = card_type
        self.name = name
        self.action_factory = action_factory
        self.speed = speed
        self.target_checker = target_checker
        self.scene_id = getter.register(self)
        self.location = location
        if location is not None:
            location.add_card(self)

    def move(self, new_location):
        self.location.remove_card(self)
        new_location.add_card(self)

    def resolve(self, player, target_list):
        if not self.target_checker(target_list):
            raise IndexError
        self.action_factory(player, target_list)
        self.move(player.discardpile)

    def __str__(self) -> str:
        my_string = create_tag("card_type", self.card_type)
        my_string += create_tag("name", self.name)
        my_string += create_tag("action_factory", str(self.action_factory))
        my_string += create_tag("speed", self.speed.name)
        my_string += create_tag("target_checker", str(self.target_checker))
        my_string += create_tag("location", self.location.scene_id)
        my_string += create_tag("scene_id", self.scene_id)
        return my_string

    @classmethod
    def create_from_string(cls, string: str):
        possible_filename = detag_given_tags("file")
        if len(possible_filename) == 1:
            with open(root_path(*possible_filename)) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        card_type, name, action_factory, speed, target_checker, location_string = detag_given_tags(string, "card_type",
                                                                                                   "name",
                                                                                                   "action_factory",
                                                                                                   "speed",
                                                                                                   "target_checker",
                                                                                                   "location")
        action_factory = Action_Factory.create_from_string(action_factory)
        speed = Speed[speed]
        target_checker = getattr(TargetChecker, target_checker)
        if location_string == "":
            location = None
        else:
            location = getter[int(location_string)]
        result = Card(card_type, name, action_factory, speed, target_checker, location)
        scene_id, = detag_given_tags(string, "scene_id")
        if scene_id != "" and scene_id != "auto":
            getter[int(scene_id)] = result
        return result

    def __eq__(self, other):
        return str(self) == str(other)


def create_card(cardname, location) -> Card:
    my_card = cards_by_string[cardname](location)
    location.add_card(my_card)
    return my_card


def create_tackle(location) -> Card:
    tackle = Card("Tackle", "Tackle", Action_Factories.tackle_factory, Speed.Fast, TargetChecker.single_target_non_card,
                  location)
    return tackle


def create_brace(location) -> Card:
    brace = Card("Brace", "Brace", Action_Factories.brace_factory, Speed.Instant, TargetChecker.no_target, location)
    return brace


cards_by_string = {
    "Tackle": lambda location: Card.load_from_file("resources/Cards/tackle.card"),
    "Brace": create_brace
}
