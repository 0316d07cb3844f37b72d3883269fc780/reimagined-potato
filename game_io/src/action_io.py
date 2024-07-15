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
    top_row = make_top_row(action)
    bottom_row = make_bottom_row(action)
    result = stack_vertical(top_row, bottom_row)
    return stack_horizontal(get_portrait(action.scene_id).image, result)


def make_top_row(action):
    performer_face = get_portrait(action.performer.scene_id)
    performer_face = pygame.transform.scale(performer_face.image, (90, 75))
    stability_image = make_text_field("Stability: " + str(action.stability), size=20)
    speed_image = make_text_field(action.speed.name, size=20)
    return stack_horizontal(performer_face, stack_vertical(speed_image, stability_image, offset=5))


def make_bottom_row(action):

    target_faces = [get_portrait(target.scene_id) for target in action.target_list]
    if target_faces:
        return stack_horizontal(*[pygame.transform.scale(face.image, (75,90)) for face in target_faces])
    else:
        return pygame.Surface((1, 90))


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
