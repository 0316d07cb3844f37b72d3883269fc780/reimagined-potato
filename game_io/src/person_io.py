"""
Contains a Person as rendered on screen.
"""

import pygame
from pygame.constants import RLEACCEL
from pygame.sprite import Sprite

from game_io.src.image_util import stack_vertical
from game_data.src.person_fighting import Person_Fighting
from utility.src.string_utils import root_path


class Person_IO(Sprite):

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
        Sprite.__init__(self)
        self.person_fighting = person_fighting
        self.name = name
        text_name = name
        text_health = "Health: " + str(person_fighting.base_person.health) + "/" + str(person_fighting.base_person.max_health)
        text_resist = "Resist: " + str(person_fighting.resist)
        font = pygame.font.Font(None, 36)
        text_name_render = font.render(text_name, 1, [1, 1, 1])
        text_health_render = font.render(text_health, 1, [1, 1, 1])
        text_resist_render = font.render(text_resist, 1, [1, 1, 1])
        self.image = stack_vertical(image, text_name_render, text_health_render, text_resist_render)
        self.rect = self.image.get_rect()
        self.rect.center = position


type_to_looks = {
    "Testtype": ("Testbert", "resources/testguy.bmp")
}
