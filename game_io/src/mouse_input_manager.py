"""Creates an input object to be consumed by the top layer under the mouse."""
from enum import Enum

import pygame
from pygame import mouse
from types import SimpleNamespace


class InputType(Enum):
    consumed = 0
    no_input = 1
    click = 2
    hold = 3
    release = 4
    scroll_up = 5
    scroll_down = 6
    drag = 7


class MouseInput:
    def __init__(self, input_type=InputType.no_input, position=(0, 0), delta=(0, 0)):
        self.input_type = input_type
        self.position = position
        self.delta = delta


def update_mouse_input():
    global mouse_input
    if mouse.get_pressed()[0]:
        if mouse_input.input_type in (InputType.no_input, InputType.release):
            input_type = InputType.click
        else:
            input_type = InputType.hold
    mouse_input = MouseInput(input_type=SimpleNamespace(), position=mouse.get_pos())


def get_mouse_input():
    global mouse_input
    result = mouse_input
    mouse_input = MouseInput(input_type=InputType.consumed, position=(0, 0))
    return result


mouse_input = SimpleNamespace()
