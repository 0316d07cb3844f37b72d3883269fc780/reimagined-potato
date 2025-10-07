from typing import Callable

from game_data.src.atomic_event import AtomicEvent, EventType
from game_data.src.getterscene import getter


class ReplacementEffect:
    def __init__(self, applies: Callable, replace: Callable, priority):
        self.applies = applies
        self.replace = replace
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority


def is_action_resolving(event, scene):
    return event.event_type == EventType.resolve_action


def replace_action_resolving(event: AtomicEvent):
    action = getter[event.action]
    events = action.resolve()
    events.append(event)
    return events


def did_ally_die(event, scene):
    return event.event_type == EventType.destroy and getter[event.destroyed] in scene.allies


def replace_ally_died(event: AtomicEvent):
    return [AtomicEvent(EventType.foes_won)]



action_resolve_replacement = ReplacementEffect(is_action_resolving, replace_action_resolving, 10)

ally_dying_replacement = ReplacementEffect(did_ally_die, replace_ally_died, 1000)

built_in_replacements = [action_resolve_replacement]
