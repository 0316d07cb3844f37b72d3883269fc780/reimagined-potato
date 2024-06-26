"""
Contains utility functions for building images to display.
"""

import pygame
from pygame import RLEACCEL
import pygame.freetype
from pygame.transform import scale

from utility.src.string_utils import root_path

pygame.freetype.init()
font_path = root_path("resources/Fonts/NotoSerif-Regular.ttf")
font_path_bold = root_path("resources/Fonts/NotoSerif-Bold.ttf")
font_path_italic = root_path("resources/Fonts/OpenSans-Italic-VariableFont_wdth,wght.ttf")


def stack_vertical(*images, offset=0):
    """
    Return a vertical stack of images.
    """
    width = max([image.get_width() for image in images])
    height = sum([image.get_height() for image in images])+offset*(len(images)-1)
    composite = pygame.Surface([width, height])
    composite.fill([1, 2, 3])
    composite.set_colorkey(composite.get_at((0, 0)))

    # blit images
    bottom_end = 0
    middle = width / 2
    for image in images:
        rect = image.get_rect()
        rect.midtop = [middle, bottom_end]
        composite.blit(image, rect)
        bottom_end += image.get_height()+offset
    return composite


def stack_horizontal(*images, offset=0):
    """
    Return a vertical stack of images.
    """
    width = sum([image.get_width() for image in images])+offset*(len(images)-1)
    height = max([image.get_height() for image in images])
    composite = pygame.Surface([width, height])
    composite.fill([1, 2, 3])
    composite.set_colorkey(composite.get_at((0, 0)))

    # blit images
    right_end = 0
    middle = height / 2
    for image in images:
        rect = image.get_rect()
        rect.midleft = [right_end, middle]
        composite.blit(image, rect)
        right_end += image.get_width()+offset
    return composite


def make_text_field(text: str, size=36, bgcolor=[240,240,240], rect=None):
    """
    Return a surface with the given text on it
    :param text: The text to display.
    :param size: Textsize
    :param rect: Optional size of the surface, if none is given the surface will have the appropriate size.
    :return: The surface.
    """
    lines = text.splitlines()
    font = pygame.freetype.Font(font_path, size)

    renders = [font.render(line, fgcolor=[0, 0, 0], bgcolor=bgcolor, style=pygame.freetype.STYLE_NORMAL)[0] for line in lines]
    text_render = stack_vertical(*renders, offset=2)
    text_render.set_colorkey(bgcolor)
    if rect is None:
        return text_render
    result = pygame.Surface(rect.size)
    result.fill(bgcolor)
    text_rect = text_render.get_rect()
    text_rect.center = rect.center
    result.blit(text_render, text_rect)
    result.set_colorkey(bgcolor)
    return result


def make_image(path: str, opaque: bool = False):
    try:
        image = pygame.image.load(root_path(path))
    except pygame.error as message:
        print("Cannot load: " + path)
        raise SystemExit(message)
    image = image.convert()
    if not opaque:
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
    return image


def scaled_by_half(image):
    half_size = [i // 2 for i in image.get_size()]
    return scale(image, half_size)
