"""
Attribute of a card responsible for generating actions when the card resolves.
"""

from game_data.src.action import create_tackle, create_brace
from enum import Enum


class Action_Factory():
    def __init__(self, factory_method, name):
        self.factory_method = factory_method
        self.factory_name = name
        Factories[name] = self

    def __call__(self, performer, target_list):
        return self.factory_method(performer, target_list)

    def __str__(self):
        return self.factory_name

    def __eq__(self, other):
        if (not hasattr(other, "factory_name")):
            return False
        return (self.factory_name == other.factory_name) & (self.factory_method == self.factory_method)

    @classmethod
    def create_from_string(cls, string):
        return Factories[string]


Factories = {}


class Action_Factories(Action_Factory, Enum):
    def __new__(cls, method, name):
        obj = Action_Factory(method, name)
        obj._value_ = obj
        return obj

    tackle_factory = (create_tackle, "Tackle_Factory")
    brace_factory = (create_brace, "Brace_Factory")


def create_from_string(string):
    return Factories[string]
