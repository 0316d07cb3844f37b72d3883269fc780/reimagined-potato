from game_data.src.card import TargetChecker


class TargetFinderSimple:
    def __init__(self, scene):
        self.scene = scene

    def find_targets(self, card):
        if card.target_checker == TargetChecker.no_target:
            return [[]]
        elif card.target_checker == TargetChecker.single_target_non_card:
            result = [[person.scene_id] for person in self.scene.all_people]
            result += [[action.scene_id] for action in self.scene.actions]
            result += [[stance.scene_id] for stance in self.scene.stances]
            return result
        elif card.target_checker == TargetChecker.single_target_person:
            return [[person.scene_id] for person in self.scene.all_people]
        elif card.target_checker == TargetChecker.single_target_action_or_stance:
            result = [[action.scene_id] for action in self.scene.actions]
            result += [[stance.scene_id] for stance in self.scene.stances]
            return result

