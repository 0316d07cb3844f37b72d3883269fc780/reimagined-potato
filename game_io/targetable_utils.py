from pygame import Surface
from pygame.surfarray import pixels3d


def image_to_images_hovered_and_pressed(surface: Surface) -> list:
    result = [surface, surface.copy(), surface.copy()]
    hovered = pixels3d(result[1])
    pressed = pixels3d((result[2]))
    hovered * 0.8 + 50
    pressed * 0.7 + 3
    return result

