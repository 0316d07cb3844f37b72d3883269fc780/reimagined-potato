"""
Interface for Conditionboards.
"""

from abc import ABCMeta, abstractmethod


class ConditionBoard(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "parse_event") and callable(subclass.parse_event) \
               and hasattr(subclass, "event_happened") and callable(subclass.event_happened)

    @abstractmethod
    def parse_event(self, event):
        raise NotImplementedError

    @abstractmethod
    def condition_holds(self) -> bool:
        raise NotImplementedError
