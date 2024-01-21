import unittest
import pygame
import time
from game_data.src.fight_scene import Fight_Scene
from game_io.src.scene_aranger import *
from game_io.src.sprite_manager import SpriteManager


class VisualTest(unittest.TestCase):

    def test_initialize_two_dogs_from_file(self):
        pygame.init()
        clock = pygame.time.Clock()
        scene_data = Fight_Scene.create_scene_from_string("<file>resources/Scenes/two_dogs_fighting.scene<\\file>")
        sprite_manager = SpriteManager()
        initialize_scene(scene_data, 0, sprite_manager.allsprites, sprite_manager.hand_sprites)
        while True:
            clock.tick(60)
            pygame.event.get()
            sprite_manager.do_frame()





if __name__ == '__main__':
    unittest.main()
