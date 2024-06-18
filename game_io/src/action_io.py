import csv

import pygame

from game_data.src.action import Action
from game_io.src.button import Button
from game_io.src.image_util import *
from game_io.src.targetable_utils import *
from game_io.src.portrait_io import get_portrait
from game_io.src.getter_io import getter
from game_io.src.client_event_builder import builder


class ActionIO(Button):

    def __init__(self, action: Action, position=None):
        self.action = action
        image = make_action_image(action)
        self.rect = image.get_rect()
        if position is not None:
            self.rect.center = position
        getter[action.scene_id] = self
        super().__init__(image_to_images_hovered_and_pressed(image), self.rect)
        builder.register_targetable(self)

    def redraw_self(self):
        image = make_action_image(self.action)
        self.image = image
        self.background_images = image_to_images_hovered_and_pressed(self.image)


def make_action_image(action):
    name_image = make_text_field(action.name)
    middle_row = make_middle_row(action.stability, action.speed)
    bottom_row = make_bottom_row(action)
    result = stack_vertical(name_image, middle_row, bottom_row)
    return stack_horizontal(make_left_main_part(action), result)


def make_left_main_part(action):
    performer_face = get_portrait(action.performer.scene_id)
    action_image = get_portrait(action.scene_id)
    return stack_horizontal(performer_face.image, action_image.image)


def make_middle_row(stability, speed):
    stability_image = make_text_field("Stability: " + str(stability))
    speed_image = make_text_field(speed.name)
    return stack_horizontal(stability_image, speed_image)


def make_bottom_row(action):

    target_faces = [get_portrait(scene_id) for scene_id in action.target_list]
    if target_faces:
        return stack_horizontal(*target_faces)
    else:
        return pygame.Surface((1, 180))


def get_action_image(action_id):
    if action_id in action_image_by_id:
        return action_image_by_id[action_id]
    else:
        return make_image(image_path_by_id[action_id])


image_path_by_id = {}

with open(root_path("resources/Actions/actions.csv")) as actions_file:
    csvreader = csv.reader(actions_file, delimiter=";")
    next(csvreader)
    for row in csvreader:
        action_id = row[1]
        action_image_path = row[2]
        image_path_by_id[int(action_id)] = action_image_path

action_image_by_id = {}
