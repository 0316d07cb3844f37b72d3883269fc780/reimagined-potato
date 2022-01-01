"""
Carries all state of a combat encounter.
"""

from enum import Enum


class Fight_Scene():
    def __init__(self, allies, foes):
        """

        :param allies:
        :param foes:
        """
        Check_params(allies, foes)
        self.allies = allies
        self.foes = foes
        self.turn_side = Turn.allies
        self.turn_index = 1


class Turn(Enum):
    allies = 0
    foes = 1


def Check_params(allies, foes):
    if len(allies) == 0 | len(foes) == 0:
        raise IndexError("Not enough participants for fight scene.")
