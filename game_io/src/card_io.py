from game_io.src.button import Button
from game_data.src.card import Card
from game_io.src.image_util import *
from game_io.src.targetable_utils import *


class CardIO(Button):
    def __init__(self, card: Card, center_position):
        self.card_data = card
        image = make_card_image(card)
        self.rect = self.image.get_rect()
        self.rect.center = center_position
        super().__init__(image_to_images_hovered_and_pressed(image), rect=self.rect)


def make_card_image(card: Card):
    top_row = make_top_row(card.name, card.speed)
    if card.card_type in type_to_image:
        image = type_to_image[card.card_type]
    else:
        image = make_image(type_to_image_path[card.card_type])
        type_to_image[card.card_type] = image
    textfield = make_text_field(type_to_card_text[card.card_type])
    return stack_vertical(top_row, image, textfield)


def make_top_row(name, speed):
    name_render = make_text_field(name, rect=(0, 0, 300, 100))
    speed_render = make_text_field(speed.name, rect=(0, 0, 100, 100))
    return stack_horizontal(name_render, speed_render)


type_to_image_path = {
    "Tackle": "",
    "Brace": ""
}

type_to_image = {}

type_to_card_text = {
    "Tackle": "",
    "Brace": ""
}
