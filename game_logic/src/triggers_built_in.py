from game_data.src.atomic_event import EventType as ET
from game_data.src.atomic_event import AtomicEvent as AE


def redraw(events, _, fight_scene):
    result = []
    for event in events:
        if event.event_type == ET.redraw_hands:
            for fighter in fight_scene.all_people:
                for card in fighter.hand:
                    result.append(AE(ET.discard, discarded_card=card.scene_id, discarder=fighter.scene_id))
                result.append(AE(ET.draw_card, drawer=fighter.scene_id))
    return result


def resolve_action(events, getter, _):
    result = []
    for event in events:
        if event.event_type == ET.resolve_action:
            action = getter[event.action]
            result.extend(action.resolve())
    return result

def allies_lost(events, _, fight_scene):
    result=[]
    for event in events:
        if event.event_type == ET.destroy and event.destroyed in fight_scene.allies:
            result.append(AE(ET.foes_won))
    return result

builtins = [

    redraw,
    resolve_action,


]
