"""
Contains the underlying data of a Card inside a scene.
"""

class Card():
    def __init__(self, name, action_factory, speed, ID):
        self.name=name
        self.action_factory=action_factory
        self.speed= speed
        self.ID = ID


from enum import Enum

class Speed(Enum):
    Regular=1
    Fast=2
    Instant=3

from game_data.src.action import create_tackle
Tackle=Card("Tackle",create_tackle, Speed.Fast, 1)