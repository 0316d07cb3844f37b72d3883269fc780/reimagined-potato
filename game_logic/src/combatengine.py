"""
Runs all the computations.
"""
from game_data.src.fight_scene import Fight_Scene
from game_logic.src.scene_transformer import transform
from game_data.src.getter_scene import getter
from game_data.src.atomic_event import *

from itertools import chain


class CombatEngine:
    def __init__(self, networker_wrapper, fight_scene=None):
        self.fight_scene = fight_scene
        self.networker_wrapper = networker_wrapper
        self.next_task = None
        self.atomic_events_scheduled = []
        self.atomic_events_history = []

    def engine_loop(self):
        while True:
            if len(self.atomic_events_scheduled) is not 0:
                next_event = self.get_next_atomic_event()
                to_do = self.apply_replacements(next_event)
                for event in to_do:
                    self.process_atomic_event(event)
                self.atomic_events_scheduled += self.triggered_events(to_do)
                self.check_state_based_actions()
                self.send_out_history()
                continue
            list_of_client_events = self.networker_wrapper.get_all_messsages()
            for event in list_of_client_events:
                self.process_client_event(event)

    def check_state_based_actions(self):
        state_based_to_do = []

        self.check_if_fight_over(state_based_to_do)
        self.check_if_someone_died_from_damage(state_based_to_do)
        self.check_if_turn_over(state_based_to_do)

        state_based_to_do = sum([self.apply_replacements(atomic_event) for atomic_event in state_based_to_do])
        for event in state_based_to_do:
            self.process_atomic_event(event)
        if len(state_based_to_do) > 0:
            self.check_state_based_actions()

    @staticmethod
    def apply_replacements(event):
        return [event]

    def triggered_events(self, list_of_events):
        result = []
        return result

    def get_next_atomic_event(self):
        return self.atomic_events_scheduled.pop(0)

    def process_atomic_event(self, event):
        transform(event, getter, self.fight_scene)
        self.atomic_events_history.append(event)

    def process_client_event(self, event):
        if event.event_type == "set_fightscene":
            self.fight_scene = event.fight_scene
        if event.event_type == "PLAY_CARD":
            atomic_event = AtomicEvent(EventType.play_card, card=event.card, player=event.player, )
        if event.event_type == "END_TURN":
            atomic_event = AtomicEvent(EventType.pass_priority, passer=event.player)
        self.atomic_events_scheduled.append(atomic_event)

    def send_out_history(self):
        result = ""
        for event in self.atomic_events_history:
            result += create_tag("event", str(event))
        self.networker_wrapper.send_to_all_players(result)
        self.atomic_events_history.clear()

    def check_if_turn_over(self, todo):
        if all([person.turn_ended for person in self.fight_scene.current_side]):
            todo.append(AtomicEvent(EventType.change_sides))


    def check_if_someone_died_from_damage(self, todo):
        for person in self.fight_scene.all_people:
            if person.health <= 0:
                todo.append(EventSomethingDied(person.scene_id))
        for damagable in chain (self.fight_scene.actions, self.fight_scene.stances):
            if damagable.stability <= 0:
                todo.append(EventSomethingDied(damagable.scene_id))

    def check_if_fight_over(self, todo):
        pass

