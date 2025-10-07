"""One selfcontained screen that manages its own layering and priorities."""
import pygame


class Screen:
    def __init__(self, layers: list, priority: int = 0, enabled: bool = False):
        self.layers = layers
        self.priority = priority
        self.enabled = enabled

    def update(self) -> None:
        for layer in self.layers[::-1]:
            layer.update()

    def draw(self, surface: pygame.Surface) -> None:
        for layer in self.layers:
            layer.draw(surface)
