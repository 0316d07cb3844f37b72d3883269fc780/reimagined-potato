from math import inf
from main import get_engine_events
from game_data.src.getterscene import GetterScene, getter
from game_data.src.fight_scene import Fight_Scene, Side
import game_data.src.getterscene as gs_module
from game_logic.src.combatengine import CombatEngine
from game_logic.src.serverNetworkerWrapper import ClientEvent, MockPassWrapper
from game_logic.src.client_networker import Client_Networker
from game_logic.src.scene_transformer import transform
from ai.hardcoded.src.target_finder import TargetFinderSimple

from game_data.src.fight_scene import Fight_Scene


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
        highest_outcome = -inf
        chosen_move = None
        for move in possible_moves:
            with lambda: SceneCopier(self.scene) as scene_copier:
                outcome = self.evaluate_outcome_pre(move)
                scene = scene_copier.make_scene()
                emulator = CombatEngine(MockPassWrapper(None), scene)
                emulator.networker_wrapper.engine = emulator
                emulator.networker_wrapper.set_next_messages([move])
                emulator.simulate_until_stack_is_clear()
                outcome += self.evaluate_outcome_post()
                if outcome > highest_outcome:
                    highest_outcome = outcome
                    chosen_move = move
        return chosen_move

    def find_legal_moves(self):
        my_guy = getter[self.scene_id_character]
        moves = [ClientEvent.create_end_turn_generating_string(self.scene_id_character)]
        for card in my_guy.hand:
            possible_lists_of_targets = self.targetfinder.find_targets(card)
            for targets in possible_lists_of_targets:
                moves.append(ClientEvent.create_play_card_generating_string(self.scene_id_character, card.scene_id, targets))
        return moves

    def evaluate_outcome_pre(self, move):
        result = 0
        return 0

    def evaluate_outcome_post(self):
        enemy_team_life_sum = sum([person.base_person.health + person.resist for person in self.enemy_team])
        own_team_life_sum = sum([person.base_person.health + person.resist for person in self.enemy_team])
        return own_team_life_sum - enemy_team_life_sum


class SceneCopier:
    def __init__(self, scene):
        self.scene = scene

    def __enter__(self):
        self.getter_original = gs_module.getter
        gs_module.getter = GetterScene()

    def __exit__(self, exc_type, exc_val, exc_tb):
        gs_module.getter = self.getter_original

    def make_scene(self):
        return Fight_Scene.create_scene_from_string(str(self.scene))


def ai_loop(scene: Fight_Scene, scene_id_character: int):
    networker = Client_Networker(patient=True)
    targetfinder = TargetFinderSimple(scene)
    ai = Ai(scene, scene_id_character, targetfinder)
    running = True
    while running:
        events = get_engine_events(networker)
        for event in events:
            transform(event, getter, scene)
        networker.send(ai.find_best_move())

