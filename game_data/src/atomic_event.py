from enum import Enum
from utility.src.string_utils import *


class EventType(Enum):
    play_card = "Play Card"
    create_action = "Create Action"
    create_stance = "Create Stance"
    target = "Target"
    untarget = "Untarget"
    pass_priority = "Pass Priority"
    change_sides = "Change Sides"
    damage = "Damage"
    draw_card = "Card Draw"
    destroy = "Destroy"
    discard = "Discard Card"


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


class EventPlayCard(AtomicEvent):
    def __init__(self, card_scene_id, player_scene_id, targets_scene_ids):
        super().__init__(EventType.play_card,
                         Card_Scene_Id=card_scene_id,
                         Card_Player=player_scene_id,
                         Targets_Scene_Id=targets_scene_ids)