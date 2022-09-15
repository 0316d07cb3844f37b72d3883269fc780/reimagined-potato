"""
Carries all state of a combat encounter.
"""

from enum import Enum
from utility.src.string_utils import create_tag, detag_given_tags,detag_repeated
from game_data.src.person_fighting import Person_Fighting
from game_data.src.action import Action


class Side(Enum):
    allies = 0
    foes = 1


class Fight_Scene():
    def __init__(self, allies : list, foes : list, actions : list = []):
        """

        :param allies:
        :param foes:
        """

        self.allies = allies
        self.foes = foes
        self._turn_side = Side.allies
        self.turn_index = 1
        self.actions = actions

    @property
    def current_side(self) -> str:
        return getattr(self, self._turn_side.name)

    def change_turn(self) -> None:
        if self._turn_side == Side.allies:
            self._turn_side = Side.foes
        else:
            self._turn_side = Side.allies
        for person in self.current_side:
            person.turn_ended=False

    def side_to_string(self, side : Side) -> str:
        side=getattr(self, side.name)
        return ", ".join([create_tag("fighter" ,lad) for lad in side])

    @classmethod
    def create_team_from_string(cls, string: str) -> list:
        fighter_strings = detag_repeated(string, "fighter")
        return [Person_Fighting.create_from_string(fighter) for fighter in fighter_strings]

    @classmethod
    def create_scene_from_string(cls, string: str):
        allies_string, foes_string = detag_given_tags(string, "allies", "foes")
        actions_string, = detag_given_tags(string, "actions")
        list_of_action_strings = detag_repeated(actions_string, "action")
        actions = [Action.create_from_string(string) for string in list_of_action_strings]
        return Fight_Scene(Fight_Scene.create_team_from_string(allies_string), Fight_Scene.create_team_from_string(foes_string), actions)








