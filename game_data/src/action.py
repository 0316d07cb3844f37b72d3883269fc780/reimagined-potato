"""
An action that a person will perform at the end of the turn.
"""

from enum import Enum

from game_data.src.getter_scene import getter
from utility.src.string_utils import create_tag, get_id_list, detag_given_tags, root_path


class Speed(Enum):
    Channel = 0
    Regular = 1
    Fast = 2
    Instant = 3


class Action:
    def __init__(self, name: str, performer, target_list: list, method: callable, speed: Speed, stability: int,
                 action_id: int):
        self.name = name
        self.performer = performer
        self.target_list = target_list
        self.method = method
        self.speed = speed
        self.stability = stability
        self.action_id = action_id
        performer.append_action(self)

    def __str__(self) -> str:
        my_string = create_tag("name", self.name)
        my_string += create_tag("performer_id", self.performer.scene_id)
        my_string += create_tag("target_id_list", [target.scene_id for target in self.target_list])
        my_string += create_tag("speed", self.speed.name)
        my_string += create_tag("stability", self.stability)
        my_string += create_tag("action_id", self.action_id)
        return my_string

    @classmethod
    def create_from_string(cls, string: str):
        possible_filename = detag_given_tags("file")
        if len(possible_filename) == 1:
            with open(root_path(*possible_filename)) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        tags = "name", "performer_id", "target_id_list", "stability", "action_id"
        name, performer_id, target_id_list, stability, action_id = detag_given_tags(string, *tags)
        target_id_list = get_id_list(target_id_list)
        performer_id = int(performer_id)
        action_id = int(action_id)
        target_list = [getter[target_id] for target_id in target_id_list]
        action = creator_by_id[action_id](getter[performer_id], target_list)
        action.stability = stability
        return action

    def resolve(self) -> None:
        self.method(self.performer, self.target_list)


def tackle_method(_, tackled_list):
    tackled_list[0].damage(6)


def create_tackle(tackler, tackled_list: list) -> Action:
    tackle = Action("Tackle", tackler, tackled_list, tackle_method, Speed.Fast, 3, 1)
    return tackle


def brace_method(bracer, _):
    bracer.resist += 4


def create_brace(bracer, braced=None) -> Action:
    return Action("Brace", bracer, [], brace_method, Speed.Instant, 3, 2)


creator_by_id = {
    1: create_tackle,
    2: create_brace
}
