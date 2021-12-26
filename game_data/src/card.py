"""
Contains the underlying data of a Card inside a scene.
"""

class Card():
    last_id=0
    all_cards={}
    def __init__(self, name, action_factory, speed, target_checker, location):
        self.name=name
        self.action_factory=action_factory
        self.speed= speed
        self.target_checker=target_checker
        self.ID = Card.last_id
        Card.last_id +=1
        Card.all_cards[self.ID]=self
        self.location = location
        location.add_card(self)

    def move(self, new_location):
        self.location.remove_card(self)
        new_location.add_card(self)

    def resolve(self, player, target_list):
        if not self.target_checker(target_list):
            raise IndexError
        self.action_factory(player, target_list)


from enum import Enum

class Speed(Enum):
    Channel=0
    Regular=1
    Fast=2
    Instant=3

class Target_Checker(Enum):
    no_target = lambda targetlist:len(targetlist)==0
    singletarget=lambda targetlist:len(targetlist)==1



def create_card(cardname,location):
    return create_tackle(location)

from game_data.src.action import create_tackle as create_tackle_action
def create_tackle(location):
    Tackle=Card("Tackle",lambda tackler, tackled :create_tackle_action(tackler,tackled[0]), Speed.Fast,Target_Checker.singletarget,location)
    return Tackle