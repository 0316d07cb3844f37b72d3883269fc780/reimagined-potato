import unittest
from multiprocessing import Event

from ai.src.ai import Ai, AiLooper
from ai.hardcoded.src.target_finder import TargetFinderSimple
from game_logic.src.scene_transformer import transform
from game_data.src.fight_scene import Fight_Scene
from game_logic.src.client_networker import Client_Networker, get_engine_events, MockNetworker
from game_data.src.getterscene import GetterScene, getter


class MyTestCase(unittest.TestCase):
    def test_loop(self):
        mock_networker = MockNetworker(message_file="ai/test/ressources/ai_test_messages")
        ailooper = AiLooper("<file>resources/Scenes/two_dogs_fighting.scene<\\file>", 32, Event(), mock_networker)
        ailooper.loop()



if __name__ == '__main__':
    unittest.main()
