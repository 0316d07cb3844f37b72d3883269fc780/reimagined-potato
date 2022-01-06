import unittest

from game_data.src.fight_scene import Fight_Scene as Scene
from game_data.src.fight_scene import Side
from test_person_fighting import make_person


def make_game_state():
    allies, foes = [], []

    for _ in range(4):
        ally, foe = make_person(), make_person()
        allies.append(ally)
        foes.append(foe)
    return Scene(allies, foes)


class MyTestCase(unittest.TestCase):
    def test_make_game_state(self):
        my_state = make_game_state()

    def test_string_side(self):
        my_state= make_game_state()
        my_string=my_state.side_to_string(Side.allies)
        Scene.create_team_from_string(my_string)

    def test_sides(self):
        my_state = make_game_state()
        self.assertTrue(my_state.current_side==my_state.allies)
        my_state.change_turn()
        self.assertTrue(my_state.current_side == my_state.foes)
        my_state.change_turn()
        self.assertTrue(my_state.current_side == my_state.allies)


if __name__ == '__main__':
    unittest.main()
