import unittest
from game_data.src.fight_scene import Fight_Scene
from game_io.src.scene_aranger import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        scene_data = Fight_Scene.create_scene_from_string("<file>resources/Scenes/two_dogs_fighting.scene<\\file>")



if __name__ == '__main__':
    unittest.main()
