import pygame
import pygame.font
from pygame import mouse
from enum import Enum

class State(Enum):
    NEUTRAL=0
    HOVERED=1
    PRESSED=2

class Button (pygame.sprite.Sprite):


    def __init__(self, text, background_images, rect, on_click=[]):
        pygame.sprite.Sprite.__init__(self)
        # set up text
        font = pygame.font.Font(None , 36)
        text_render = font.render(text,1,[1,1,1])
        text_pos=text_render.get_rect(centerx=background_images[0].get_width() / 2)
        for i in range(3):
            background_images[i].blit(text_render, text_pos)

        # visuals
        self.background_images=background_images
        self.text = text
        self.image, self.rect = background_images[0], rect
        self.on_click = on_click

        # internal state
        self.state=State.NEUTRAL

    def update(self, *args, **kwargs) -> None:
        Button.updater.get(self.state)(self)

    def update_neutral(self):
        if(self.rect.collidepoint(mouse.get_pos()) and not mouse.get_pressed()[0]):
            self.state=State.HOVERED
            self.image=self.background_images[1]
            self.update()

    def update_hovered(self):
        if(not self.rect.collidepoint(mouse.get_pos())):
            self.image=self.background_images[0]
            self.state=State.NEUTRAL
        else:
            if (mouse.get_pressed()[0]):
                [todo() for todo in self.on_click]
                self.image=self.background_images[2]
                self.state=State.PRESSED
    def update_pressed(self):
        if (not mouse.get_pressed()[0]):
            self.image=self.background_images[1]
            self.state = State.HOVERED
            self.update()


    updater={
        State.NEUTRAL:update_neutral,
        State.HOVERED:update_hovered,
        State.PRESSED:update_pressed
    }



