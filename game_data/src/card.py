"""
Contains the underlying data of a Card inside a scene.
"""

class Card():
    last_id=0
    all_cards={}
    def __init__(self, name, action_factory, speed, location):
        self.name=name
        self.action_factory=action_factory
        self.speed= speed
        self.ID = Card.last_id
        Card.last_id +=1
        Card.all_cards[self.ID]=self
        self.location = location
        location.add_card(self)

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
    Tackle=Card("Tackle",lambda tackler, tackled :create_tackle_action(tackler,tackled[0]), Speed.Fast,location)
    return Tackle