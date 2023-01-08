"""
Attribute of a card responsible for generating actions when the card resolves.
"""


from game_data.src.action import *
from enum import Enum


class Action_Factory:
    def __init__(self, factory_method, name : str):
        self.factory_method = factory_method
        self.factory_name = name
        Factories[name] = self

    def __call__(self, performer, target_list):
        return self.factory_method(performer, target_list)

    def __str__(self) -> str:
        return self.factory_name

    def __eq__(self, other):
        if (not hasattr(other, "factory_name")):
            return False
        return (self.factory_name == other.factory_name) & (self.factory_method == self.factory_method)

    @classmethod
    def create_from_string(cls, string):
        return Factories[string]


Factories = {}


class ActionFactories(Action_Factory, Enum):
    def __new__(cls, method, name):
        obj = Action_Factory(method, name)
        obj._value_ = obj
        return obj

    tackle_factory = (create_tackle, "Tackle_Factory")
    brace_factory = (create_brace, "Brace_Factory")
    side_step_factory = (create_side_step, "Sidestep_Factory")
    crushing_blow_factory = (create_crushing_blow, "Crushing_Blow_Factory")
    tail_swipe_factory = (create_tail_swipe, "Tail_Swipe_Factory")
    reckless_assault_factory = (create_reckless_assault, "Reckless_Assault_Factory")
    bark_skin_blessing_factory = (create_bark_skin_blessing, "Bark_Skin_Blessing_Factory")
    engulf_in_flames_factory = (create_engulf_in_flames, "Engulf_In_Flames_Factory")
    sunshine_blessing_factory = (create_sunshine_blessing, "Sunshine_Blessing_Factory")
    mind_blast_factory = (create_mind_blast, "Mind Blast Factory")

