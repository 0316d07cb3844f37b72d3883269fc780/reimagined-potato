import pygame
import pygame.font
from pygame import mouse
from enum import Enum

class State(Enum):
    NEUTRAL=0
    HOVERED=1
    PRESSED=2

class Button (pygame.sprite.Sprite):


    def __init__(self, text, background_image, rect, on_click=[]):
        pygame.sprite.Sprite.__init__(self)
        # set up text
        font = pygame.font.Font(None , 36)
        text_render = font.render(text,1,[1,1,1])
        text_pos=text_render.get_rect(centerx=background_image.get_width()/2)
        background_image.blit(text_render, text_pos)

        # visuals
        self.text = text
        self.image, self.rect = background_image, rect
        self.on_click = on_click

        # internal state
        self.state=State.NEUTRAL

    def update(self, *args, **kwargs) -> None:
        Button.updater.get(self.state)(self)

    def update_neutral(self):
        if(self.rect.collidepoint(mouse.get_pos())):
            self.state=State.HOVERED
            self.update()

    def update_hovered(self):
        if(not self.rect.collidepoint(mouse.get_pos())):
            self.state=State.NEUTRAL
        else:
            if (mouse.get_pressed()[0]):
                [todo() for todo in self.on_click]
                self.state=State.PRESSED
    def update_pressed(self):
        if (not mouse.get_pressed()[0]):
            self.state = State.HOVERED


    updater={
        State.NEUTRAL:update_neutral,
        State.HOVERED:update_hovered,
        State.PRESSED:update_pressed
    }



