import unittest
from copy import deepcopy

from game_data.src.fight_scene import Fight_Scene as Scene
from game_data.src.fight_scene import Side
from game_data.src.getterscene import getter
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
        make_game_state()

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

    def test_state_to_string_and_back(self):
        my_state=make_game_state()
        my_string=str(my_state)
        Scene.create_scene_from_string(my_string)

    def test_make_from_file(self):
        my_scene = Scene.create_scene_from_string("<file>resources/Scenes/two_dogs_fighting.scene<\\file>")
        ally_dog = my_scene.allies[0]
        enemy_dog = my_scene.foes[0]
        self.assertTrue(enemy_dog.turn_ended)
        self.assertTrue(not ally_dog.turn_ended)

    def test_register(self):
        my_scene = make_game_state()
        my_scene = deepcopy(my_scene)
        my_scene.reregister()
        for person in my_scene.all_people:
            self.assertTrue(person is getter[person.scene_id])


if __name__ == '__main__':
    unittest.main()
