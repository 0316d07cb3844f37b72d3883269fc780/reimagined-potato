import unittest
from ai.src.ai import Ai
from ai.hardcoded.src.target_finder import TargetFinderSimple
from game_logic.src.scene_transformer import transform
from game_data.src.fight_scene import Fight_Scene
from game_logic.src.client_networker import Client_Networker, get_engine_events, MockNetworker
from game_data.src.getterscene import GetterScene, getter


class MyTestCase(unittest.TestCase):
    def test_loop(self):
        networker = MockNetworker()

        def ai_loop(scene_string: str, scene_id_character: int):
            scene = Fight_Scene.create_scene_from_string(scene_string)
            networker.introduce_self(scene_id_character)
            targetfinder = TargetFinderSimple(scene)
            ai = Ai(scene, scene_id_character, targetfinder)
            running = True
            my_guy = getter[scene_id_character]
            while running:
                events = get_engine_events(networker)
                for event in events:
                    transform(event, getter, scene)
                if not my_guy.turn_ended:
                    networker.send(ai.find_best_move())
        ai_loop("<file>resources/Scenes/two_dogs_fighting.scene<\\file>", 30)


if __name__ == '__main__':
    unittest.main()
