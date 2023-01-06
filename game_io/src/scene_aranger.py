"""Add a sprite for every data object in a fight scene to a group of sprites and wire them up."""
from game_data.src.fight_scene import Fight_Scene, Side
from pygame.sprite import RenderPlain
import game_io.src.scene_constants as constants
from game_io.src.action_io import ActionIO
from game_io.src.stance_io import StanceIO
from game_io.src.card_io import CardIO
from game_io.src.personio import PersonIO


def initialize_scene(scene: Fight_Scene, index_player: int, scene_group: RenderPlain, hand_group: RenderPlain):
    """
    Creates all the necessary objects in the right places.
    :param index_player: The character controlled by this client.
    :param scene: Data Objects to be rendered.
    :param scene_group: Group for actions at the top of the screen and people and stances in the middle.
    :param hand_group: Group for cards in hand, possibly overlaps with scene group.
    :return: Nothing
    """
    initialize_actions(scene.actions, scene_group)
    initialize_people(scene.allies, scene.foes, scene_group)
    initialize_hand(scene.allies[index_player].hand, hand_group)


def initialize_actions(actions: list, scene_group: RenderPlain):
    last_edge_middle = (0, constants.ACTIONS_ROW_CENTER_HEIGHT)
    for action in actions:
        action_io = ActionIO(action)
        action_widths = action_io.rect.width
        last_edge_middle[0] += action_widths
        action_io.rect.midright = last_edge_middle
        scene_group.add(action_io)


def initialize_people(allies: list, foes: list, scene_group: RenderPlain):
    for index, ally in enumerate(allies):
        horizontal_position_person = calculate_horizontal_position_person(index, Side.allies)
        horizontal_position_stance = horizontal_position_person - (constants.PERSON_WIDTHS+constants.STANCE_SPACE_WIDTHS)//2
        ally_io = PersonIO(ally, (horizontal_position_person, constants.PEOPLE_ROW_CENTER_HEIGHT))
        scene_group.add(ally_io)
        initialize_stances(ally.stances, horizontal_position_stance, scene_group)

    for index, foe in enumerate(foes):
        horizontal_position_person = calculate_horizontal_position_person(index, Side.foes)
        horizontal_position_stance = horizontal_position_person + (constants.PERSON_WIDTHS+constants.STANCE_SPACE_WIDTHS)//2
        foe_io = PersonIO(foe, (horizontal_position_person, constants.PEOPLE_ROW_CENTER_HEIGHT))
        scene_group.add(foe_io)
        initialize_stances(foe.stances, horizontal_position_stance, scene_group)


def calculate_horizontal_position_person(index_person, team: Side):
    offset_from_center = (constants.GAP_PEOPLE + constants.PERSON_WIDTHS)//2
    offset_from_center += index_person * (constants.GAP_PEOPLE + constants.PERSON_WIDTHS + constants.STANCE_SPACE_WIDTHS)
    if team is Side.allies:
        offset_from_center = -offset_from_center
    return constants.PEOPLE_ROW_CENTER_WIDTH + offset_from_center


def initialize_stances(stances: list, horizontal_center: int, scene_group: RenderPlain):
    last_edge_bottom = (horizontal_center, constants.PEOPLE_ROW_TOP)
    for stance in stances:
        stance_io = StanceIO(stance)
        stance_io.rect.midtop = last_edge_bottom
        last_edge_bottom = stance_io.rect.midbottom
        scene_group.add(stance_io)


def initialize_hand(hand, hand_group):
    last_right_edge = (0, constants.HAND_ROW_CENTER_HEIGHT)
    for card in hand:
        card_io = CardIO(card)
        last_right_edge[0] += constants.CARD_WIDTH
        card_io.rect.midright = last_right_edge
        hand_group.add()

