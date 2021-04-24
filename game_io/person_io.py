"""
Contains a Person as rendered on screen.
"""

from pygame.sprite import Sprite

class Person_IO(Sprite):
    def __init__(self, person_data, image, position, name):
        """

        :param person_data: Underlying Data Object
        :param image: Character image
        :param position: Where to render the center of the person
        :param name: Person's name
        """
        self.person_data=person_data
        self.image=image
        self.name=name

        self.rect= None


