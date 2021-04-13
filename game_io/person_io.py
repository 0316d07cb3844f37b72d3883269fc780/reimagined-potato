"""
Contains a Person as rendered on screen.
"""

from pygame.sprite import Sprite

class Person_IO(Sprite):
    def __init__(self, person_data, image, rect, name):
        self.person_data=person_data
        self.image=image
        self.rect=rect
        self.name=name


