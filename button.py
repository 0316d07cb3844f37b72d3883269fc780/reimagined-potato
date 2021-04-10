import pygame
import pygame.font
from pygame import mouse

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

    def update(self, *args, **kwargs) -> None:
        if(mouse.get_pressed()[0]):
            [todo() for todo in self.on_click]


