"""
A stance a person controls. It passively affects transitions in game state and can be destroyed.
"""

from game_data.src.loadable import Loadable
from game_data.src.getterscene import getter
from utility.src.string_utils import *
from game_data.src.stance_triggers import trigger_by_stance_id


class Stance(Loadable):

    def __init__(self, name: str, performer, target_list: list, stability: int,
                 stance_id: int):
        self.name = name
        self.performer = performer
        self.target_list = target_list
        self.stability = stability
        self.count = 1
        self.stance_id = stance_id
        self.scene_id = getter.register(self)
        performer.append_action(self)

    def __str__(self):
        my_string = create_tag("name", self.name)
        my_string += create_tag("performer_id", self.performer.scene_id)
        my_string += create_tag("target_id_list", [target.scene_id for target in self.target_list])
        my_string += create_tag("count", self.count)
        my_string += create_tag("stability", self.stability)
        my_string += create_tag("stance_id", self.stance_id)
        my_string += create_tag("scene_id", self.scene_id)
        return my_string

    @classmethod
    def create_from_string(cls, string: str):
        possible_filename = detag_given_tags("file")
        if len(possible_filename) == 1:
            with open(root_path(*possible_filename)) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        tags = "name", "performer_id", "target_id_list", "stability", "count", "stance_id", "scene_id"
        name, performer_id, target_id_list, stability, count, stance_id, scene_id = detag_given_tags(string, *tags)
        target_id_list = get_id_list(target_id_list)
        performer_id = int(performer_id)
        stance_id = stance_id
        target_list = [getter[target_id] for target_id in target_id_list]
        stance = Stance(name, getter[performer_id], target_list, stability, stance_id)
        stance.count = count
        getter[scene_id] = stance
        return stance

    def damage(self, damage_amount):
        self.stability -= max(damage_amount, 0)

    def get_destroyed(self):
        del self

    @property
    def blueprint_id(self):
        return self.stance_id

    @property
    def triggers(self):
        return trigger_by_stance_id[self.stance_id]


substitutors_by_id = {

}