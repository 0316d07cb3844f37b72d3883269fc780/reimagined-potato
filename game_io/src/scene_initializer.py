"""Add a sprite for every data object in a fight scene to a group of sprites and wire them up."""
from game_data.src.fight_scene import Fight_Scene
from pygame.sprite import RenderPlain
import game_io.src.scene_constants as constants


def initialize_scene(scene: Fight_Scene, scene_group: RenderPlain, hand_group: RenderPlain):
    """
    Creates all the necessary objects in the right places.
    :param scene: Data Objects to be rendered.
    :param scene_group: Group for actions at the top of the screen and people and stances in the middle.
    :param hand_group: Group for cards in hand, possibly overlaps with scene group.
    :return: Nothing
    """
    initialize_actions(scene.actions, scene_group)
    initialize_people(scene.allies, scene.foes, scene_group)
    initialize_stances(scene.stances, scene_group)
    initialize_hand(hand_group)


def initialize_actions(actions: list, scene_group: RenderPlain):
    pass


def initialize_people(allies: list, foes: list, scene_group: RenderPlain):
    pass


def initialize_stances(stances: list, scene_group: RenderPlain):
    for stance in stances:
        pass


def initialize_hand(hand, hand_group):
    pass
