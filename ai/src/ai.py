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
        chosen_move = possible_moves[0]
        outcome_pre= self.evaluate_outcome()
        highest_outcome = self.evaluate_outcome_pass()
        emulator = CombatEngine(MockPassWrapper(None))
        for move in possible_moves[1:]:
            with SceneCopier.make_copier(scene) as scene_copier:
                scene = scene_copier.make_scene()
                scene_original = self.scene
                self.scene = scene
                emulator.fight_scene = scene
                emulator.networker_wrapper.engine = emulator
                emulator.networker_wrapper.set_next_messages([move])
                emulator.simulate_until_stack_is_clear()
                outcome = self.evaluate_outcome()-outcome_pre
                if outcome > highest_outcome:
                    highest_outcome = outcome
                    chosen_move = move
                self.scene = scene_original
        return chosen_move

    def evaluate_outcome_pass(self):
        amount_own_team_moves_on_stack = len(
            [action for action in self.scene.actions if action.performer in self.own_team])
        amount_enemy_team_moves_on_stack = len(
            [action for action in self.scene.actions if action.performer in self.enemy_team])
        cards_in_own_teams_hands = sum([len(person.hand) for person in self.own_team])
        cards_in_enemy_teams_hands = sum([len(person.hand) for person in self.enemy_team])
        penalty_moves_on_stack = amount_own_team_moves_on_stack
        penalty_more_moves_on_stack_than_enemies = (amount_own_team_moves_on_stack-amount_enemy_team_moves_on_stack) * 2
        if not self.scene.actions:
            penalty_less_cards_than_enemy = 5 * max(0, cards_in_enemy_teams_hands-cards_in_own_teams_hands)
        else:
            penalty_less_cards_than_enemy = 0
        return penalty_moves_on_stack + penalty_more_moves_on_stack_than_enemies + penalty_less_cards_than_enemy - 1

    def find_legal_moves(self):
        my_guy = getter[self.scene_id_character]
        moves = [ClientEvent.create_end_turn_generating_string(self.scene_id_character)]
        for card in my_guy.hand:
            possible_lists_of_targets = self.targetfinder.find_targets(card)
            for targets in possible_lists_of_targets:
                moves.append(
                    ClientEvent.create_play_card_generating_string(self.scene_id_character, card.scene_id, targets))
        return moves

    def evaluate_outcome(self):
        enemy_team_life_sum = sum([person.base_person.health + person.resist for person in self.enemy_team])
        own_team_life_sum = sum([person.base_person.health + person.resist for person in self.own_team])
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

    @staticmethod
    def make_copier(scene: Fight_Scene):
        """
        Creates a SceneCopier that copies the given scene.
        :param scene: The scene to copy.
        :return: A SceneCopier instance.
        """
        return SceneCopier(scene)


def ai_loop(scene_string: str, scene_id_character: int):
    scene = Fight_Scene.create_scene_from_string(scene_string)
    networker = Client_Networker(patient=True, log_recieve_seperately=True)
    networker.introduce_self(scene_id_character)
    targetfinder = TargetFinderSimple(scene)
    ai = Ai(scene, scene_id_character, targetfinder)
    running = True
    my_guy = getter[scene_id_character]
    while running:
        events = get_engine_events(networker)
        for event in events:
            if event.event_type == "set_scene":
                scene = Fight_Scene.create_scene_from_string(event.fight_scene)
            transform(event, getter, scene)
        if not my_guy.turn_ended:
            networker.send(ai.find_best_move())
