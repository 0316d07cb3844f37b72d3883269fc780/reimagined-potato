import copy
import unittest

from game_data.src.atomic_event import EventType
from game_data.src.fight_scene import Fight_Scene
from game_logic.src.combatengine import CombatEngine


class TestTheChecks(unittest.TestCase):
    def test_check_if_turn_over(self):
        my_wrapper = MockedWrapper()
        engine = get_engine(my_wrapper)
        self.assertEqual(engine.fight_scene.current_side, engine.fight_scene.allies)
        engine.check_if_turn_over([])
        self.assertEqual(engine.fight_scene.current_side, engine.fight_scene.allies)
        for guy in engine.fight_scene.allies:
            guy.turn_ended = True
        engine.check_if_turn_over([])
        self.assertEqual(engine.fight_scene.current_side, engine.fight_scene.foes)

    def test_check_if_someone_died_from_damage(self):
        my_wrapper = MockedWrapper()
        engine = get_engine(my_wrapper)
        engine.fight_scene.foes[0].damage(10000)
        todo = []
        engine.check_if_someone_died_from_damage(todo)
        event, = todo
        self.assertEqual(EventType.destroy, event.event_type)

    def test_check_if_fight_over(self):
        my_wrapper = MockedWrapper()
        engine = get_engine(my_wrapper)
        engine.fight_scene.foes = []
        todo = []
        engine.check_if_fight_over(todo)
        event, = todo
        self.assertEqual(EventType.allies_won, event.event_type)


class MockedWrapper:
    pass


def get_engine(wrapper: MockedWrapper):
    my_scene = copy.deepcopy(scene)
    my_engine = CombatEngine(wrapper, my_scene)
    return my_engine


scene = Fight_Scene.create_scene_from_string("<file>resources/Scenes/two_dogs_fighting.scene<\\file>")

if __name__ == '__main__':
    unittest.main()
