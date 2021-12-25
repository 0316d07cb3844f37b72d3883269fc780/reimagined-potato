"""
Contains the underlying data of a Card inside a scene.
"""

class Card():
    last_id=0
    def __init__(self, name, action_factory, speed, location):
        self.name=name
        self.action_factory=action_factory
        self.speed= speed
        self.ID = Card.last_id
        Card.last_id +=1
        self.location = location

    def move(self, new_location):
        self.location.remove_card(self)
        new_location.add_card(self)


from enum import Enum

class Speed(Enum):
    Regular=1
    Fast=2
    Instant=3

def create_card(cardname,location):
    return create_tackle(location)

from game_data.src.action import create_tackle as create_tackle_action
def create_tackle(location):
    Tackle=Card("Tackle",create_tackle_action, Speed.Fast,location)
    return Tackle