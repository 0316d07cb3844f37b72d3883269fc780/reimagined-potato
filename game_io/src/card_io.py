from pygame.sprite import Sprite

from game_data.src.card import Card
from game_io.src.image_util import *


class CardIO(Sprite):
    def __init__(self, card: Card):
        super().__init__()
        self.card_data = card
        self.image = make_card_image(card)
        self.rect = self.image.get_rect()


def make_card_image(card: Card):
    top_row = make_top_row(card.name, card.speed)
    image = make_image(type_to_image_path[card.card_type])
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

type_to_card_text = {
    "Tackle": "",
    "Brace": ""
}
