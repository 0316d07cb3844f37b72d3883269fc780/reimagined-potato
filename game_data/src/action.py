"""
An action that a person will perform at the end of the turn.
"""

from utility.src.string_utils import create_tag, get_id_list, detag_given_tags
from game_data.src.getter_scene import getter


class Action():
    def __init__(self, name : str, performer, target_list : list, method : callable, id : int):
        self.name = name
        self.performer = performer
        self.target_list = target_list
        self.method = method
        self.action_id = id
        performer.append_action(self)

    def __str__(self) -> str:
        my_string = create_tag("name", self.name)
        my_string += create_tag("performer_id", self.performer.scene_id)
        my_string += create_tag("target_id_list", [target.scene_id for target in self.target_list])
        my_string += create_tag("action_id", self.action_id)
        return my_string

    @classmethod
    def create_from_string(cls, string : str) :
        tags = "name", "performer_id", "target_id_list", "action_id"
        name, performer_id, target_id_list, id = detag_given_tags(string, *tags)
        target_id_list = get_id_list(target_id_list)
        performer_id = int(performer_id)
        id = int(id)
        target_list = [getter[target_id] for target_id in target_id_list]
        return creator_by_id[id](getter[performer_id], target_list)

    def resolve(self) -> None:
        self.method(self.performer, self.target_list)


tackle_method = lambda tackler, tackled_list: tackled_list[0].damage(6)


def create_tackle(tackler, tackled_list:list)->Action:
    tackle = Action("Tackle", tackler, tackled_list, tackle_method, 1)
    return tackle


def brace_method(bracer, brace_targets):
    bracer.resist += 4


def create_brace(bracer, braced=None) -> Action:
    return Action("Brace", bracer, [], brace_method, 2)


creator_by_id = {
    1: create_tackle,
    2: create_brace
}
