"""
Runs all the computations.
"""
from game_data.src.fight_scene import Fight_Scene
from game_logic.src.scene_transformer import transform
from game_data.src.getter_scene import getter
from game_data.src.atomic_event import *


class CombatEngine:
    def __init__(self, fight_scene=None):
        self.fight_scene = fight_scene
        self.next_task = None
        self.atomic_events_scheduled = []
        self.atomic_events_history = []

    def engine_loop(self):
        while True:
            if len(self.atomic_events_scheduled) is not 0:
                next_event = self.get_next_atomic_event()
                to_do = self.apply_replacements(next_event)
                for event in to_do:
                    transform(getter, event)
                    self.check_state_based_actions()
                self.atomic_events_history += to_do
                self.atomic_events_scheduled += self.triggered_events(to_do)
            self.check_state_based_actions()

    def check_state_based_actions(self):
        state_based_to_do = []

        self.check_if_fight_over(state_based_to_do)
        self.check_if_someone_died(state_based_to_do)
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
        transform(getter, event)
        self.atomic_events_history.append(event)

    def process_client_event(self, event):

        if event.event_type=="PLAY_CARD":
            event.cards.resolve(event.player, event.target_list)
            event.player.turn_ended = True
            return
        if event.event_type=="END_TURN":
            pass

    def check_if_turn_over(self, todo):
        if all([person.turn_ended for person in self.fight_scene.current_side]):
            todo.append(AtomicEvent(EventType.change_sides))

    def check_if_someone_died(self, todo):
        pass

    def check_if_fight_over(self, todo):
        pass


class ClientEvent:

    def __init__(self, string):
        type, = detag_given_tags(string, "type")
        if type == "set_fightscene":
            scene_string = detag_given_tags(string, "scene")
            self.fight_scene = Fight_Scene.create_scene_from_string()
        player_id, = detag_given_tags(string, "player_id")
        self.player = getter[int(player_id)]
        if type == "END_TURN":
            self.event_type = "END_TURN"
            return
        if type == "PLAY_CARD":
            card_id, target_id_list = detag_given_tags(string, "card_id", "target_id_list")
            self.event_type = "PLAY_CARD"
            self.card = getter[int(card_id)]
            self.target_list = [getter[int(target_id)] for target_id in target_id_list]

