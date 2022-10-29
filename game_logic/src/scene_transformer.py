from game_data.src.atomic_event import EventType as et

def transform(atomic_event, getter,  scene):
    """
    Takes a scene getter and performs single atomic transformation.
    :param getter:
    :param atomic_event:
    :return:
    """
    event_type, attributes = atomic_event.event_type, atomic_event.attributes
    if event_type == et.play_card:
        getter[atomic_event.card].resolve(getter[atomic_event.player], getter[atomic_event.target_list])
        atomic_event.player.turn_ended = True
    elif event_type == et.target:
        pass
    elif event_type == et.untarget:
        pass
    elif event_type == et.pass_priority:
        pass
    elif event_type == et.damage:
        pass
    elif event_type == et.draw_card:
        pass
    elif event_type == et.destroy:
        pass
    elif event_type == et.discard:
        pass
