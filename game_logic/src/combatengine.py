"""
Runs all the computations.
"""
import itertools
from itertools import chain, product
from typing import Callable

from game_data.src.atomic_event import *
from game_data.src.getterscene import getter
from game_logic.src.replacement_effect import built_in_replacements
from game_logic.src.scene_transformer import transform
from game_logic.src.triggers_built_in import builtins as builtin_triggers


class CombatEngine:
    def __init__(self, networker_wrapper, fight_scene=None):
        self.fight_scene = fight_scene
        self.networker_wrapper = networker_wrapper
        self.next_task = None
        self.atomic_events_scheduled = []
        self.atomic_events_history = []
        self.keep_running = True
        self.something_happened = False

    def engine_loop(self):
        def check_keep_running():
            return self.keep_running

        self.abstract_loop(check_keep_running)

    def abstract_loop(self, running_checker):
        while running_checker():
            self.clear_out_atomic_events()
            if self.something_happened:
                self.networker_wrapper.send_to_all_players(create_tag("event", AtomicEvent(EventType.engine_done)))
                self.something_happened = False
            if not running_checker():
                break
            list_of_client_events = self.networker_wrapper.get_all_messages()
            for event in list_of_client_events:
                self.process_client_event(event)

    def clear_out_atomic_events(self):
        """
        Simulate the game state forward until client input is necessary.
        """
        if self.atomic_events_scheduled:
            next_event = self.get_next_atomic_event()
            to_do = self.apply_replacements(next_event)
            for event in to_do:
                self.process_atomic_event(event)
            self.check_state_based_actions()
            self.send_out_history()
            self.clear_out_atomic_events()

    def process_atomic_event(self, event):
        self.fight_scene.reregister()
        transform(event, getter, self.fight_scene)
        triggered_events = self.triggered_events([event])
        self.atomic_events_scheduled.extend(triggered_events)
        self.atomic_events_history.append(event)

    def check_state_based_actions(self):
        state_based_to_do = []
        work_was_done_flag = False
        checks = [self.check_if_someone_died_from_damage,
                  self.check_if_fight_over,
                  self.check_if_turn_over]

        for check in checks:
            assert isinstance(check, Callable)
            check(state_based_to_do)
            state_based_to_do = chain(*[self.apply_replacements(atomic_event) for atomic_event in state_based_to_do])
            for event in state_based_to_do:
                self.process_atomic_event(event)
                self.atomic_events_scheduled.extend(self.triggered_events(state_based_to_do))
                work_was_done_flag = True
            state_based_to_do = []

        if work_was_done_flag:
            self.check_state_based_actions()

    @staticmethod
    def apply_replacements(event):
        result = [event]
        replacements = built_in_replacements[:]
        replacements.sort()
        while any([replacement.applies(event) for replacement, event in itertools.product(replacements, result)]):
            next_replacement = next(
                replacement for replacement in replacements if any([replacement.applies(event) for event in result]))
            replacements.remove(next_replacement)
            result = sum([next_replacement.replace(event) for event in result], start=[])
        return result

    def triggered_events(self, list_of_events):
        result = []
        for event, trigger in product(list_of_events, self.triggers):
            result.extend(trigger(event, getter, self.fight_scene))
        return result

    @property
    def triggers(self):
        result = [stance.triggers for stance in self.fight_scene.stances]
        result += builtin_triggers
        return result

    def get_next_atomic_event(self):
        return self.atomic_events_scheduled.pop(0)

    def process_client_event(self, event):
        atomic_event = None
        if event.event_type == "set_fightscene":
            self.fight_scene = event.fight_scene
        elif event.event_type == "START_SCENE":
            atomic_event = AtomicEvent(EventType.redraw_hands)
        elif event.event_type == "PLAY_CARD":
            if self.check_input(event):
                atomic_event = EventPlayCard(event.card.scene_id, event.player.scene_id,
                                             [target.scene_id for target in event.target_list])
        elif event.event_type == "END_TURN":
            if self.check_input(event):
                atomic_event = AtomicEvent(EventType.pass_priority, passer=event.player.scene_id)
        elif event.event_type == "ACCEPT_CONNECTION":
            self.networker_wrapper.networker.check_for_connection()
        elif event.event_type == "END_ENGINE":
            self.keep_running = False
        elif event.event_type == "Introduction":
            self.networker_wrapper.send_to_player(create_tag("event", set_scene(str(self.fight_scene))),
                                                  event.person_id)
        if atomic_event:
            self.atomic_events_scheduled.append(atomic_event)
            self.something_happened = True

    def check_input(self, event):
        player = getter[event.player.scene_id]
        if player.turn_ended:
            return False
        if event.event_type == "PLAY_CARD":
            return getter[event.card.scene_id] in player.hand
        elif event.event_type == "END_TURN":
            return True

    def send_out_history(self):
        result = ""
        for event in self.atomic_events_history:
            result += create_tag("event", str(event))
        self.networker_wrapper.send_to_all_players(result)
        self.atomic_events_history.clear()

    def check_if_turn_over(self, _):
        if all([person.turn_ended for person in self.fight_scene.current_side]):
            self.process_atomic_event(AtomicEvent(EventType.change_sides))
            if not self.fight_scene.actions:
                self.atomic_events_scheduled.append(AtomicEvent(EventType.redraw_hands))
            else:
                for action in self.fight_scene.actions[::-1]:
                    if any([(action is fighter.actions[-1] if fighter.actions else False) for fighter in
                            self.fight_scene.current_side]):
                        event = AtomicEvent(EventType.resolve_action, action=action.scene_id)
                        self.atomic_events_scheduled.append(event)
                    else:
                        break

    def check_if_someone_died_from_damage(self, todo):
        for person in self.fight_scene.all_people:
            if person.get_health() <= 0:
                todo.append(EventSomethingDied(person.scene_id))
        for damagable in chain(self.fight_scene.actions, self.fight_scene.stances):
            if damagable.stability <= 0:
                todo.append(EventSomethingDied(damagable.scene_id))

    def check_if_fight_over(self, todo):
        if not self.fight_scene.foes:
            todo.append(AtomicEvent(EventType.allies_won))

    def simulate_until_stack_is_clear(self):
        def check_if_stack_is_clear():
            return not self.fight_scene.actions

        self.abstract_loop(check_if_stack_is_clear)

    def simulate_one_stack_resolution(self):
        stack_size = len(self.fight_scene.actions)
        if stack_size == 0:
            return
        top_action = self.fight_scene.actions[-1]

        def check_if_one_action_got_resolved():
            return self.fight_scene.actions[-1] is not top_action

        self.abstract_loop(check_if_one_action_got_resolved())
