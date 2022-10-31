from game_data.src.atomic_event import EventType as et
from game_data.src.person_fighting import Person_Fighting

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
        getter[atomic_event.player.turn_ended] = True
    elif event_type == et.target:
        getter[atomic_event.action].targetlist.append(getter[atomic_event.targeted])
    elif event_type == et.untarget:
        getter[atomic_event.action].targetlist.remove(getter[atomic_event.targeted])
    elif event_type == et.pass_priority:
        getter[atomic_event.passer].turn_ended = True
    elif event_type == et.damage:
        getter[atomic_event.damaged].damage(getter[atomic_event].damage)
    elif event_type == et.draw_card:
        getter[atomic_event.drawer].draw_Card()
    elif event_type == et.destroy:
        destroyed = getter[atomic_event.destroyed]
        if isinstance(destroyed, Person_Fighting):
            destroyed.die()
        else:
            destroyed.get_destroyed()
    elif event_type == et.discard:
        getter[atomic_event.discarded_card].move(getter[atomic_event].discarder.discardpile)
