from game_data.src.atomic_event import EventType as et
from game_data.src.person_fighting import Person_Fighting


def transform(atomic_event, getter, scene):
    """
    Takes a scene getter and performs single atomic transformation.
    :param atomic_event: What happened here.
    :param getter: Getter of Objects to transform
    :param scene: The scene to transform.
    :return:
    """
    event_type, attributes = atomic_event.event_type, atomic_event.attributes
    if event_type == et.play_card:
        getter[atomic_event.card].resolve(getter[atomic_event.player], getter[atomic_event.target_list], scene)
    elif event_type == et.create_action:
        pass
    elif event_type == et.create_stance:
        pass
    elif event_type == et.target:
        getter[atomic_event.action].targetlist.append(getter[atomic_event.targeted])
    elif event_type == et.untarget:
        getter[atomic_event.action].targetlist.remove(getter[atomic_event.targeted])
    elif event_type == et.pass_priority:
        getter[atomic_event.passer].turn_ended = True
    elif event_type == et.change_sides:
        scene.change_turn()
        for person in scene.current_side:
            person.turn_ended = False
    elif event_type == et.damage:
        try:
            for target in getter[atomic_event.damaged]:
                target.damage(atomic_event.damage)
        except TypeError:
            getter[atomic_event.damaged].damage(atomic_event.damage)
    elif event_type == et.add_resist:
        getter[atomic_event.beneficiary].resist += atomic_event.resist
    elif event_type == et.draw_card:
        getter[atomic_event.drawer].draw_card()
    elif event_type == et.destroy:
        destroyed = getter[atomic_event.destroyed]
        if isinstance(destroyed, Person_Fighting):
            destroyed.die()
        else:
            destroyed.get_destroyed()
    elif event_type == et.discard:
        getter[atomic_event.discarded_card].move(getter[atomic_event.discarder].discardpile)
    elif event_type == et.resolve_action:
        action = getter[atomic_event.action]
        action.resolve()
        scene.actions.remove(action)
    elif event_type == et.set_scene:
        pass
