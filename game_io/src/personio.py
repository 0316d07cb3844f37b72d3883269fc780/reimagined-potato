"""
Contains a Person as rendered on screen.
"""

import pygame
from pygame.constants import RLEACCEL
from pygame.transform import scale
from pygame.sprite import Sprite

from game_io.src.image_util import stack_vertical, make_text_field
from game_data.src.person_fighting import Person_Fighting
from utility.src.string_utils import root_path
from game_io.src.button import Button
from game_io.src.targetable_utils import *
from game_io.src.getter_io import getter


class PersonIO(Button):

    def __init__(self, person_fighting: Person_Fighting, position):
        """
        Create a Person to be displayed.
        :param person_fighting: Underlying Data Object
        :param position: Where to render the center of the person
        """
        name, imagelocation = type_to_looks[person_fighting.base_person.person_type]
        try:
            image = pygame.image.load(root_path(imagelocation))
        except pygame.error as message:
            print("Cannot load: " + imagelocation)
            raise SystemExit(message)
        image = image.convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        half_size = [i//2 for i in image.get_size()]
        image = scale(image, half_size)
        self.person_fighting = person_fighting
        self.name = name
        text_name = name
        text_health = "Health: " + str(person_fighting.base_person.health) + "/" + str(person_fighting.base_person.max_health)
        text_resist = "Resist: " + str(person_fighting.resist)
        text_name_render = make_text_field(text_name)
        text_health_render = make_text_field(text_health)
        text_resist_render = make_text_field(text_resist)
        self.image = stack_vertical(image, text_name_render, text_health_render, text_resist_render)
        self.rect = self.image.get_rect()
        self.rect.center = position
        getter[person_fighting.scene_id]=self
        super().__init__(image_to_images_hovered_and_pressed(self.image), rect=self.rect)




type_to_looks = {
    "Testtype": ("Testbert", "resources/testguy.bmp"),
    "Knight": ("Knight", "resources/People/Full_Art/Knight.png"),
    "Dog": ("Dog", "resources/People/Full_Art/Knight.png")
}
