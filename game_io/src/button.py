"""
Implements a Button functionality.
"""

import pygame
import pygame.font
from pygame import mouse
from enum import Enum


class State(Enum):
    """Encodes the state of the Button"""
    NEUTRAL = 0
    HOVERED = 1
    PRESSED = 2


class Button (pygame.sprite.Sprite):
    """
    A button that calls all functions on a list when pressed.
    """

    # Ensures only one button can be interacted with the mouse.
    mouse_interacted_with_button = False

    def __init__(self, background_images, rect, text="", on_click=None):
        """
        Creates a button ready to be rendered and used.
        :param text: Text on the button.
        :param background_images: A list of three images for the unpressed, hovered and pressed button.
        :param rect: Rect for rendering.
        :param on_click: List of functions to be called when the button is clicked.
        """
        pygame.sprite.Sprite.__init__(self)
        # set up text
        font = pygame.font.Font(None, 36)
        text_render = font.render(text, False, [1, 1, 1])
        text_pos = text_render.get_rect(centerx=background_images[0].get_width() / 2)
        for i in range(3):
            background_images[i].blit(text_render, text_pos)

        # visuals
        self.background_images = background_images
        self.text = text
        self.image, self.rect = background_images[0], rect
        if on_click is None:
            self.on_click = []
        else:
            self.on_click = on_click

        # internal state
        self.state = State.NEUTRAL

    def update(self, *args, **kwargs) -> None:
        """
        Updates the state of the button and calls the list of functions when clicked.

        :param args: No functionality.
        :param kwargs: No functionality.
        :return:
        """
        Button.updater.get(self.state)(self)

    def update_neutral(self):
        if self.rect.collidepoint(mouse.get_pos()) and not mouse.get_pressed()[0]:
            self.state = State.HOVERED
            self.image = self.background_images[1]
            self.update()
            Button.mouse_interacted_with_button = True

    def update_hovered(self):
        if not self.rect.collidepoint(mouse.get_pos()):
            self.image = self.background_images[0]
            self.state = State.NEUTRAL
        else:
            if mouse.get_pressed()[0]:
                [todo() for todo in self.on_click]
                self.image = self.background_images[2]
                self.state = State.PRESSED
        Button.mouse_interacted_with_button = True

    def update_pressed(self):
        if not mouse.get_pressed()[0]:
            self.image = self.background_images[1]
            self.state = State.HOVERED
            self.update()
        Button.mouse_interacted_with_button = True

    @classmethod
    def update_class(cls):
        cls.mouse_interacted_with_button = False

    updater = {
        State.NEUTRAL: update_neutral,
        State.HOVERED: update_hovered,
        State.PRESSED: update_pressed
    }



