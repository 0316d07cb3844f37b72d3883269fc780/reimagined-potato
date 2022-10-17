from enum import Enum
from utility.src.string_utils import *


class EventType(Enum):
    play_card = "Play Card"
    pass_priority = "Pass Priority"
    damage = "Damage"
    draw_card = "Card Draw"
    destroy = "Destroy"


class AtomicEvent:
    def __init__(self, event_type: EventType, **kwargs):
        """
        Describes a minimal transition from one legal fight scene state to another.
        :param event_type: The type of event
        :param kwargs: only ever use strings
        """
        self.event_type = event_type
        self.attributes = kwargs

    def __str__(self):
        result = create_tag("type", self.event_type.name)
        result += create_tag("attributes", self.attributes)
        return result

    @classmethod
    def create_from_string(cls, string: str):
        type_string, attributes = detag_given_tags(string, "type", "attributes")
        event_type = EventType[type_string]
        attributes = eval(attributes)
        return cls(event_type, **attributes)

