"""
Carries all state of a combat encounter.
"""

from enum import Enum
from utility.src.string_utils import create_tag, detag_given_tags,detag_repeated
from game_data.src.person_fighting import Person_Fighting

class Fight_Scene():
    def __init__(self, allies, foes):
        """

        :param allies:
        :param foes:
        """

        self.allies = allies
        self.foes = foes
        self.turn_side = Side.allies
        self.turn_index = 1

    def side_to_string(self, side):
        side=getattr(self, side.name)
        return ", ".join([create_tag("fighter" ,lad) for lad in side])


    @classmethod
    def create_team_from_string(cls, string):
        fighter_strings=detag_repeated(string,"fighter")
        return [Person_Fighting.create_from_string(fighter) for fighter in fighter_strings]




class Side(Enum):
    allies = 0
    foes = 1


