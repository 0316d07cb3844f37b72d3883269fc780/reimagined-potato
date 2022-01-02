"""
Contains a Person as rendered on screen.
"""

import pygame
from pygame.constants import RLEACCEL
from pygame.sprite import Sprite
from game_io.image_util import stack_vertical

class Person_IO(Sprite):



    def __init__(self, person_data, position):
        """
        Create a Person to be displayed.
        :param person_data: Underlying Data Object
        :param position: Where to render the center of the person
        """
        name, imagelocation=type_to_looks[person_data.person_type]
        try:
            image = pygame.image.load(imagelocation)
        except pygame.error as message:
            print("Cannot load: " + imagelocation)
            raise SystemExit(message)
        image = image.convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        Sprite.__init__(self)
        self.person_data=person_data
        self.name=name
        text_name =name
        text_health="Health: "+str(person_data.health)+"/"+str(person_data.max_health)
        font = pygame.font.Font(None, 36)
        text_name_render = font.render(text_name, 1, [1, 1, 1])
        text_health_render = font.render(text_health,1,[1,1,1])
        self.image = stack_vertical([image,text_name_render, text_health_render])
        self.rect= self.image.get_rect()
        self.rect.center=position




type_to_looks={
    "Testtype": ("Testbert","resources/testguy.bmp")
}
