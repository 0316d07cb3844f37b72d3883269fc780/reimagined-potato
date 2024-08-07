import csv

from game_io.src.card_io import type_to_image_path, type_to_card_text
from game_io.src.image_util import *
from game_data.src.getterscene import getter
from game_data.src.action import Action
from game_data.src.stance import Stance
from game_data.src.person_fighting import Person_Fighting


class _Portrait:
    def __init__(self, name, image_location, underlying_type, scene_id):
        self.scene_id = scene_id
        self.underlying_type = underlying_type
        name_render = make_text_field(name)
        image_render = make_image(image_location, opaque=True)
        image_render.blit(name_render, (0, 140))
        self.image = image_render


class Portrait(_Portrait):

    def __init__(self, scene_id):
        data = getter[scene_id]
        if isinstance(data, Action):
            underlying_type = "Action"
        elif isinstance(data, Stance):
            underlying_type = "Stance"
        elif isinstance(data, Person_Fighting):
            underlying_type = "Person"
        else:
            raise TypeError
        name = name_dict_by_underlying_type[underlying_type][data.blueprint_id]
        image = image_dict_by_underlying_type[underlying_type][data.blueprint_id]
        if hasattr(data, "scene_id"):
            scene_id = data.scene_id
        else:
            scene_id = None
        super().__init__(name, image, underlying_type, scene_id)


def get_portrait(scene_id):
    if scene_id in portrait_by_id:
        return portrait_by_id[scene_id]
    else:
        portrait_by_id[scene_id] = Portrait(scene_id)
        return portrait_by_id[scene_id]




portrait_by_id = {}

name_dict_by_underlying_type = {
    "Action": {

    },

    "Stance": {

    },

    "Person": {

    }
}

image_dict_by_underlying_type = {
    "Action": {

    },

    "Stance": {

    },

    "Person": {

    }


}

with open(root_path("resources/Actions/actions.csv")) as actions_file:
    csvreader = csv.reader(actions_file, delimiter=";")
    next(csvreader)
    for row in csvreader:
        name = row[0]
        action_id = int(row[1])
        action_portrait_path = row[3]
        name_dict_by_underlying_type["Action"][action_id] = name
        image_dict_by_underlying_type["Action"][action_id] = action_portrait_path

with open(root_path("resources/People/people.csv")) as people_file:
    csvreader = csv.reader(people_file, delimiter=";")
    next(csvreader)
    for row in csvreader:
        Type = row[0]
        image_path= row[1]
        portrait_path = row[2]
        name_dict_by_underlying_type["Person"][Type] = Type
        image_dict_by_underlying_type["Person"][Type] = portrait_path


