from game_data.src.atomic_event import AtomicEvent as AE
from game_data.src.atomic_event import EventType as ET


def redraw(event, _, fight_scene):
    result = []
    if event.event_type == ET.redraw_hands:
        for fighter in fight_scene.all_people:
            for card in fighter.hand:
                result.append(AE(ET.discard, discarded_card=card.scene_id, discarder=fighter.scene_id))

            result += [(AE(ET.draw_card, drawer=fighter.scene_id)) for _ in range(5)]
    return result


builtins = [

    redraw,

]
