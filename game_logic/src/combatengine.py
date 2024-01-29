"""
Runs all the computations.
"""
from itertools import chain
from typing import Callable

from game_data.src.atomic_event import *
from game_data.src.getterscene import getter
from game_logic.src.scene_transformer import transform


class CombatEngine:
    def __init__(self, networker_wrapper, fight_scene=None):
        self.fight_scene = fight_scene
        self.networker_wrapper = networker_wrapper
        self.next_task = None
        self.atomic_events_scheduled = []
        self.atomic_events_history = []
        self.keep_running = True

    def engine_loop(self):
        while self.keep_running:
            if self.atomic_events_scheduled:
                next_event = self.get_next_atomic_event()
                to_do = self.apply_replacements(next_event)
                for event in to_do:
                    self.process_atomic_event(event)
                self.check_state_based_actions()
                self.send_out_history()
                continue
            list_of_client_events = self.networker_wrapper.get_all_messages()
            for event in list_of_client_events:
                self.process_client_event(event)

    def check_state_based_actions(self):
        state_based_to_do = []
        work_was_done_flag = False
        checks = [self.check_if_someone_died_from_damage,
                  self.check_if_turn_over,
                  self.check_if_fight_over]

        for check in checks:
            assert isinstance(check, Callable)
            check(state_based_to_do)
            state_based_to_do = sum([self.apply_replacements(atomic_event) for atomic_event in state_based_to_do])
            for event in state_based_to_do:
                self.process_atomic_event(event)
                self.atomic_events_scheduled.append(self.triggered_events([state_based_to_do]))
            if state_based_to_do:
                work_was_done_flag = True
            state_based_to_do.clear()

        if work_was_done_flag:
            self.check_state_based_actions()

    @staticmethod
    def apply_replacements(event):
        return [event]

    def triggered_events(self, list_of_events):
        result = []
        for event, trigger in list_of_events, self.triggers:
            result.extend(trigger(event, getter, self.fight_scene))
        return result

    @property
    def triggers(self):
        result = [stance.triggers for stance in self.fight_scene.stances]
        return result

    def get_next_atomic_event(self):
        return self.atomic_events_scheduled.pop(0)

    def process_atomic_event(self, event):
        transform(event, getter, self.fight_scene)
        triggered_events = self.triggered_events([event])
        self.atomic_events_scheduled.extend(triggered_events)
        self.atomic_events_history.append(event)

    def process_client_event(self, event):
        atomic_event = None
        if event.event_type == "set_fightscene":
            self.fight_scene = event.fight_scene
        if event.event_type == "PLAY_CARD":
            atomic_event = EventPlayCard(event.card.scene_id, event.player.scene_id,
                                         [target.scene_id for target in event.target_list])
        if event.event_type == "END_TURN":
            atomic_event = AtomicEvent(EventType.pass_priority, passer=event.player)
        if event.event_type == "END_ENGINE":
            self.keep_running = False
        self.atomic_events_scheduled.append(atomic_event)

    def send_out_history(self):
        result = ""
        for event in self.atomic_events_history:
            result += create_tag("event", str(event))
        self.networker_wrapper.send_to_all_players(result)
        self.atomic_events_history.clear()

    def check_if_turn_over(self, todo):
        if all([person.turn_ended for person in self.fight_scene.current_side]):
            self.process_atomic_event(AtomicEvent(EventType.change_sides))
            if not self.fight_scene.actions:
                self.atomic_events_scheduled.append(AtomicEvent(EventType.redraw_hands))
            else:
                for action in self.fight_scene.actions[::-1]:
                    if any([action is fighter.actions[-1] for fighter in self.fight_scene.current_side]):
                        break
                    else:
                        event = AtomicEvent(EventType.resolve_action, action=action.scene_id)
                        self.atomic_events_scheduled.append(event)

    def check_if_someone_died_from_damage(self, todo):
        for person in self.fight_scene.all_people:
            if person.health <= 0:
                todo.append(EventSomethingDied(person.scene_id))
        for damagable in chain(self.fight_scene.actions, self.fight_scene.stances):
            if damagable.stability <= 0:
                todo.append(EventSomethingDied(damagable.scene_id))

    def check_if_fight_over(self, todo):
        if not self.fight_scene.foes:
            todo.append(AtomicEvent(EventType.allies_won))
