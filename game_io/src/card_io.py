from pygame.sprite import Sprite
from game_data.src.card import Card


class CardIO(Sprite):
    def __init__(self, card : Card):
        super().__init__()
        self.card_data = card

type_to_image_path = {
    "Tackle": "",
    "Brace" : ""
}

