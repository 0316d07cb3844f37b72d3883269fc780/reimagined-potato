"""
Contains the underlying data of a Card inside a scene.
"""

from enum import Enum

from game_data.src.loadable import Loadable
from game_data.src.action import Speed
from game_data.src.action_factory import ActionFactories, Action_Factory
from game_data.src.getterscene import getter
from utility.src.string_utils import create_tag, detag_given_tags, root_path, read_and_clean_file

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_data.src.fight_scene import Fight_Scene
    from game_data.src.person_fighting import Person_Fighting


class TargetChecker(Enum):
    no_target = lambda targetlist: len(targetlist) == 0, "no_target"
    single_target_non_card = lambda targetlist: len(targetlist) == 1, "single_target_non_card"
    single_target_person = lambda targetlist: len(targetlist) == 1, "single_target_person"
    single_target_action_or_stance = lambda targetlist: len(targetlist) == 1, "single_target_action_or_stance"
    all_enemies = lambda: True, "all_enemies"

    def __str__(self):
        return self.name

    def __call__(self, target_list):
        return self.value[0](target_list)


class Card(Loadable):
    def __init__(self, card_type: str, name: str, action_factory: Action_Factory, speed: Speed,
                 target_checker: TargetChecker,
                 location, scene_id: int = None):
        self.card_type = card_type
        self.name = name
        self.action_factory = action_factory
        self.speed = speed
        self.target_checker = target_checker
        if scene_id is not None:
            self.scene_id = scene_id
            getter[self.scene_id] = self
        else:
            self.scene_id = getter.register(self)
        self.location = location
        if location is not None:
            location.add_card(self)

    def move(self, new_location):
        self.location.remove_card(self)
        new_location.add_card(self)

    def resolve(self, player, target_list, scene: 'Fight_Scene' = None):
        if not self.target_checker(target_list):
            raise IndexError
        action = self.action_factory(player, target_list)
        self.move(player.discardpile)
        if scene is not None:
            scene.actions.append(action)

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
        possible_filename, = detag_given_tags(string, "file")
        if possible_filename != "":
            file_contents = read_and_clean_file(possible_filename)
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
        if location_string == "" or (int(location_string) not in getter):
            location = None
        else:
            location = getter[int(location_string)]
        scene_id, = detag_given_tags(string, "scene_id")
        result = Card(card_type, name, action_factory, speed, target_checker, location, scene_id)
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
    tackle = Card("Tackle", "Tackle", ActionFactories.tackle_factory, Speed.Fast, TargetChecker.single_target_non_card,
                  location)
    return tackle


def create_brace(location) -> Card:
    brace = Card("Brace", "Brace", ActionFactories.brace_factory, Speed.Instant, TargetChecker.no_target, location)
    return brace


cards_by_string = {
    "Tackle": lambda location: Card.load_from_file("resources/Cards/tackle.card"),
    "Brace": lambda location: Card.load_from_file("resources/Cards/brace.card"),
    "Reckless Assault": lambda location: Card.load_from_file("resources/Cards/reckless_assault.card"),
    "Crushing Blow": lambda location: Card.load_from_file("resources/Cards/crushing_blow.card"),
}
