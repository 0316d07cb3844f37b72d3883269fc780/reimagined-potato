"""
A stance a person controls. It passively affects transitions in game state and can be destroyed.
"""

from game_data.src.loadable import Loadable
from game_data.src.getter_scene import getter
from utility.src.string_utils import *


class Stance(Loadable):

    def __init__(self, name: str, performer, target_list: list, method: callable, stability: int,
                 action_id: int):
        self.name = name
        self.performer = performer
        self.target_list = target_list
        self.stability = stability
        self.action_id = action_id
        performer.append_action(self)


    def __str__(self):
        my_string = create_tag("name", self.name)
        my_string += create_tag("performer_id", self.performer.scene_id)
        my_string += create_tag("target_id_list", [target.scene_id for target in self.target_list])
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


    def damage(self, damage_amount):
        self.stability -= damage_amount
        if self.stability <= 0:
            self.get_destroyed()

    def get_destroyed(self):
        del self


creator_by_id = {

}