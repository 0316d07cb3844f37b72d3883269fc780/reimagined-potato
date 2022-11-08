"""
Contains utility functions for building images to display.
"""

import pygame

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

