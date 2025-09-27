import unittest
from multiprocessing import Event

from ai.src.ai import AiLooper, SceneCopier
from game_data.src.fight_scene import Fight_Scene
from game_data.src.getterscene import getter
from game_logic.src.client_networker import MockNetworker


class MyTestCase(unittest.TestCase):
    def test_loop(self):
        mock_networker = MockNetworker(message_file="ai/test/ressources/ai_test_messages")
        ailooper = AiLooper("<file>resources/Scenes/two_dogs_fighting.scene<\\file>", 32, Event(), mock_networker)
        ailooper.loop()

    def test_scene_copier(self):
        scene_string = "<file>resources/Scenes/two_dogs_fighting.scene<\\file>"
        scene = Fight_Scene.create_scene_from_string(scene_string)

        class MockAi:
            def __init__(self, scene):
                self.scene = scene

        ai = MockAi(scene)

        copier = SceneCopier(scene, ai)
        last_id = getter.getter.last_id
        with copier:
            self.assertEqual(last_id, getter.getter.last_id)




if __name__ == '__main__':
    unittest.main()
