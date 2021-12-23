import unittest
from game_data.src.fight_scene import Fight_Scene as Scene
from test_person_data import make_person

def make_game_state():
    allies,foes=[],[]

    for _ in range(4):
        ally, foe=make_person(),make_person()
        allies.append(ally)
        foes.append(foe)
    return Scene(allies, foes)

class MyTestCase(unittest.TestCase):
    def test_make_game_state(self):
        my_state = make_game_state()


if __name__ == '__main__':
    unittest.main()


