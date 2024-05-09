import csv

from game_data.src.card import Card
from game_io.src.button import Button
from game_io.src.client_event_builder import builder
from game_io.src.getter_io import getter
from game_io.src.image_util import *
from game_io.src.targetable_utils import *


class CardIO(Button):
    def __init__(self, card: Card, center_position=None):
        self.card_data = card
        self.image = make_card_image(card)
        self.rect = self.image.get_rect()
        if center_position is not None:
            self.rect.center = center_position
        getter[card.scene_id] = self

        super().__init__(image_to_images_hovered_and_pressed(self.image), rect=self.rect)
        builder.register_card(self)

    def redraw_self(self):
        self.image = make_card_image(self.card_data)
        self.background_images = image_to_images_hovered_and_pressed(self.image)


def make_card_image(card: Card):
    top_row = make_top_row(card.name, card.speed)
    if card.card_type in type_to_image:
        image = type_to_image[card.card_type]
    else:
        image = make_image(type_to_image_path[card.card_type])
        type_to_image[card.card_type] = image
    textfield = make_text_field(type_to_card_text[card.card_type])
    background = make_image("resources/Cards/art/card_background.png", opaque=True)
    background.blit(stack_vertical(top_row, image, textfield), (0, 0))
    return scaled_by_half(background)


def make_top_row(name, speed):
    name_render = make_text_field(name, rect=pygame.Rect(0, 0, 280, 100))
    speed_render = make_text_field(speed.name, rect=pygame.Rect(0, 0, 120, 100))
    return stack_horizontal(name_render, speed_render)


type_to_image_path = {}
type_to_card_text = {}

with open(root_path("resources/Cards/cards.csv")) as cardfile:
    csvreader = csv.reader(cardfile, delimiter=";")
    next(csvreader)
    for row in csvreader:
        card_type = row[0]
        card_text = row[1]
        card_image_path = row[2]
        type_to_image_path[card_type] = "resources/Cards/art/" + card_image_path
        type_to_card_text[card_type] = card_text

# Only populated at runtime
type_to_image = {}
