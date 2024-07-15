from math import inf
from game_data.src.getterscene import GetterScene, getter
from game_data.src.fight_scene import Fight_Scene
import game_data.src.getterscene as gs_module
from game_logic.src.combatengine import CombatEngine
from game_logic.src.serverNetworkerWrapper import ClientEvent, MockPassWrapper

from game_data.src.fight_scene import Fight_Scene


class Ai:
    def __init__(self, scene, scene_id_character, target_finder):
        self.scene = scene
        self.scene_id_character = scene_id_character
        self.targetfinder = target_finder
        self.fake_wrapper = MockPassWrapper()

    def find_best_move(self):
        possible_moves = self.find_legal_moves()
        highest_outcome = -inf
        for move in possible_moves:
            with lambda: SceneCopier(self.scene) as scene_copier:
                scene = scene_copier.make_scene()
                emulator = CombatEngine(MockPassWrapper(None), scene)
                emulator.networker_wrapper.engine = emulator
                emulator.networker_wrapper.set_next_messages([move])


    def find_legal_moves(self):
        my_guy = getter[self.scene_id_character]
        moves = []
        moves.append(ClientEvent.create_end_turn(self.scene_id_character))
        for card in my_guy.hand:
            targets = self.targetfinder.find_targets(card)
            moves.append(ClientEvent.create_play_card(self.scene_id_character, card.scene_id, targets))
        return moves

    def evaluate_outcome(self):
        pass


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
