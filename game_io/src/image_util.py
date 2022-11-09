"""
Contains utility functions for building images to display.
"""

import pygame
from utility.src.string_utils import root_path

font_path = root_path("resources/Fonts/OpenSans-VariableFont_wdth,wght.ttf")
font_path_italic = root_path("resources/Fonts/OpenSans-Italic-VariableFont_wdth,wght.ttf")

def stack_vertical(images):
    """
    Return a vertical stack of images.
    """
    width=max([image.get_width() for image in images])
    height=sum([image.get_height() for image in images])
    composite = pygame.Surface([width,height])
    composite.fill([1,2,3])
    composite.set_colorkey(composite.get_at((0, 0)))

    #blit images
    bottom_end=0
    middle = width/2
    for image in images:
        rect = image.get_rect()
        rect.midtop=[middle,bottom_end]
        composite.blit(image,rect)
        bottom_end+=image.get_height()
    return composite


def stack_horizontal(images):
    """
    Return a vertical stack of images.
    """
    width=sum([image.get_width() for image in images])
    height=max([image.get_height() for image in images])
    composite = pygame.Surface([width,height])
    composite.fill([1,2,3])
    composite.set_colorkey(composite.get_at((0, 0)))

    #blit images
    right_end=0
    middle = height/2
    for image in images:
        rect = image.get_rect()
        rect.midright=[right_end,middle]
        composite.blit(image,rect)
        right_end+=image.get_width()
    return composite


def make_text_field(text: str, size=36, rect=None):
    """
    Return a surface with the given text on it
    :param text: The text to display.
    :param size: Textsize
    :param rect: Optional size of the surface, if none is given the surface will have the appropriate size.
    :return: The surface.
    """
    lines = text.splitlines()
    font = pygame.font.Font(font_path, size)
    renders=[font.render(line, False, [1, 1, 1]) for line in lines]
    text_render = stack_vertical(renders)
    if rect is None:
        return text_render
    result = pygame.Surface(rect)
    text_render.get_rect().center = rect.center
    result.blit(text_render, text_render.get_rect())
    return result



