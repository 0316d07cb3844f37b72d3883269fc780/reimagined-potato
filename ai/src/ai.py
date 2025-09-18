from multiprocessing import Event

import game_data.src.getterscene as gs_module
from ai.hardcoded.src.target_finder import TargetFinderSimple
from game_data.src.fight_scene import Fight_Scene
from game_data.src.fight_scene import Side
from game_data.src.getterscene import GetterScene, getter
from game_logic.src.client_networker import Client_Networker, get_engine_events
from game_logic.src.combatengine import CombatEngine
from game_logic.src.scene_transformer import transform
from game_logic.src.serverNetworkerWrapper import ClientEvent, MockPassWrapper
from game_logic.src.client_networker import get_engine_events
from game_data.src.atomic_event import EventType


class Ai:
    def __init__(self, scene, scene_id_character, target_finder):
        """

        :param scene:
        :param scene_id_character: scene_id of the character to be controlled
        :param target_finder:
        """
        self.scene = scene
        self.scene_id_character = scene_id_character
        if any([scene_id_character == character.scene_id for character in scene.allies]):
            self.side = Side.allies
            self.own_team = scene.allies
            self.enemy_team = scene.foes
        else:
            self.side = Side.foes
            self.own_team = scene.foes
            self.enemy_team = scene.allies
        self.targetfinder = target_finder
        self.fake_wrapper = MockPassWrapper(None)

    def find_best_move(self):
        possible_moves = self.find_legal_moves()
        chosen_move_string, chosen_move = possible_moves[0]
        outcome_pre = self.evaluate_outcome()
        highest_outcome = self.evaluate_outcome_pass()
        emulator = CombatEngine(MockPassWrapper(None))
        scene_copier = SceneCopier(self.scene, self)
        for move_string, move in possible_moves[1:]:
            with scene_copier:
                emulator.fight_scene = self.scene
                emulator.networker_wrapper.engine = emulator
                emulator.networker_wrapper.set_next_messages(move)
                emulator.simulate_until_stack_is_clear()
                outcome = self.evaluate_outcome()-outcome_pre
                if outcome > highest_outcome:
                    highest_outcome = outcome
                    chosen_move_string, chosen_move = move_string, move
        return chosen_move_string, chosen_move

    def evaluate_outcome_pass(self):
        amount_own_team_moves_on_stack = len(
            [action for action in self.scene.actions if action.performer in self.own_team])
        amount_enemy_team_moves_on_stack = len(
            [action for action in self.scene.actions if action.performer in self.enemy_team])
        cards_in_own_teams_hands = sum([len(person.hand) for person in self.own_team])
        cards_in_enemy_teams_hands = sum([len(person.hand) for person in self.enemy_team])
        penalty_moves_on_stack = amount_own_team_moves_on_stack
        penalty_more_moves_on_stack_than_enemies = max((amount_own_team_moves_on_stack-amount_enemy_team_moves_on_stack) * 2, 0)
        if not self.scene.actions:
            penalty_less_cards_than_enemy = 5 * max(0, cards_in_enemy_teams_hands-cards_in_own_teams_hands)
        else:
            penalty_less_cards_than_enemy = 0
        return penalty_moves_on_stack + penalty_more_moves_on_stack_than_enemies + penalty_less_cards_than_enemy - 1

    def find_legal_moves(self):
        my_guy = getter[self.scene_id_character]
        moves = [ClientEvent.create_end_turn_generating_string(self.scene_id_character)]
        self.targetfinder.scene = self.scene
        for card in my_guy.hand:
            possible_lists_of_targets = self.targetfinder.find_targets(card)
            for targets in possible_lists_of_targets:
                moves.append(
                    ClientEvent.create_play_card_generating_string(self.scene_id_character, card.scene_id, targets))
        return [(move_string, ClientEvent(move_string)) for move_string in moves]

    def evaluate_outcome(self):
        enemy_team_life_sum = sum([person.base_person.health + person.resist for person in self.enemy_team])
        own_team_life_sum = sum([person.base_person.health + person.resist for person in self.own_team])
        return own_team_life_sum - enemy_team_life_sum


class SceneCopier:
    def __init__(self, scene, ai):
        self.scene = scene
        self.ai = ai

    def __enter__(self):
        self.getter_original = gs_module.getter.getter
        gs_module.getter.getter = GetterScene()
        self.ai.scene = self.make_scene()

    def __exit__(self, exc_type, exc_val, exc_tb):
        gs_module.getter.getter = self.getter_original
        self.ai.scene = self.scene

    def make_scene(self):
        return Fight_Scene.create_scene_from_string(str(self.scene))


def ai_loop_classed(scene_string: str, scene_id_character: int, ai_runs: Event, networker=None):
    looper = AiLooper(scene_string, scene_id_character, ai_runs, networker)
    looper.loop()


class AiLooper:
    def __init__(self, scene_string: str, scene_id_character: int, ai_runs: Event, networker=None):
        scene = Fight_Scene.create_scene_from_string(scene_string)
        self.scene_id_character = scene_id_character
        self.ai_runs = ai_runs
        if networker is None:
            self.networker = Client_Networker(patient=True, log_recieve_seperately=True)
            self.networker.introduce_self(scene_id_character)
        else:
            self.networker = networker
        self.targetfinder = TargetFinderSimple(scene)
        self.ai = Ai(scene, scene_id_character, self.targetfinder)
        self.running = True

    @property
    def my_guy(self):
        return getter[self.scene_id_character]

    @property
    def scene(self):
        return self.ai.scene

    @scene.setter
    def scene(self, scene):
        self.ai.scene = scene

    def loop(self):
        engine_done_flag = False
        while self.running:
            events = get_engine_events(self.networker)
            for event in events:
                if event.event_type == EventType.set_scene:
                    self.scene = Fight_Scene.create_scene_from_string(event.scene_string)
                    self.ai_runs.set()
                if event.event_type == EventType.engine_done:
                    engine_done_flag = True
                    break
                transform(event, getter, self.scene)
            if not self.my_guy.turn_ended and engine_done_flag:
                move_string, move = self.ai.find_best_move()
                self.networker.send(move_string)
                if move.event_type == "END_TURN":
                    engine_done_flag = False

