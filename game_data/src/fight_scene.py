"""
Carries all state of a combat encounter.
"""

from enum import Enum
from itertools import chain

from game_data.src.getterscene import getter
from game_data.src.loadable import Loadable
from game_data.src.action import Action
from game_data.src.stance import Stance
from game_data.src.card import Card
from game_data.src.person_fighting import Person_Fighting
from utility.src.string_utils import read_and_clean_file, create_tag, detag_given_tags, detag_repeated, root_path


class Side(Enum):
    allies = 0
    foes = 1

    def other_side(self):
        if self == Side.allies:
            return Side.foes
        return Side.allies


class Fight_Scene(Loadable):

    def __init__(self, allies: list, foes: list, actions: list = None, stances: list = None):
        """

        :param allies:
        :param foes:
        """

        self.allies = allies
        self.foes = foes
        self._turn_side = Side.allies
        self.actions = actions
        self.stances = stances
        self.card_in_resolution = None
        self.targets_being_selected_ids = []
        if actions is None:
            self.actions = []
        if stances is None:
            self.stances = []

    def __iter__(self):
        return chain(self.allies, self.foes, self.actions, self.stances)

    def reregister(self):
        for item in self:
            getter[item.scene_id] = item

    @property
    def current_side(self):
        return getattr(self, self._turn_side.name)

    @property
    def other_side(self):
        return getattr(self, self._turn_side.other_side().name)

    @property
    def all_people(self):
        return self.allies+self.foes

    @property
    def all_objects(self):
        return self.allies + self.foes + self.actions + self.stances

    def remove_object(self, to_be_removed):
        if to_be_removed in self.actions:
            self.actions.remove(to_be_removed)
        elif to_be_removed in self.stances:
            self.stances.remove(to_be_removed)
        elif to_be_removed in self.allies:
            self.allies.remove(to_be_removed)
        elif to_be_removed in self.foes:
            self.foes.remove(to_be_removed)

    def change_turn(self) -> None:
        if self._turn_side == Side.allies:
            self._turn_side = Side.foes
        else:
            self._turn_side = Side.allies
        for person in self.current_side:
            person.turn_ended = False

    def side_to_string(self, side: Side) -> str:
        side = getattr(self, side.name)
        result = "\n".join([create_tag("fighter", lad) for lad in side])
        result = create_tag("team", result)
        return result

    @classmethod
    def create_team_from_string(cls, string: str) -> list:
        possible_filename, = detag_given_tags(string, "file")
        if possible_filename != "":
            file_contents = read_and_clean_file(possible_filename)
            return cls.create_team_from_string(file_contents)
        string_of_fighters, = detag_given_tags(string, "team")
        fighter_strings = detag_repeated(string_of_fighters, "fighter")
        return [Person_Fighting.create_from_string(fighter) for fighter in fighter_strings]

    def __str__(self):
        result = create_tag("allies", self.side_to_string(Side.allies)) \
                 + create_tag("foes", self.side_to_string(Side.foes))
        result += create_tag("turn_side", self._turn_side.name)
        action_strings = "\n".join([create_tag("action", str(action)) for action in self.actions])
        stances_strings = "\n".join([create_tag("stance", str(stance)) for stance in self.stances])
        result += create_tag("actions", action_strings)
        result += create_tag("stances", stances_strings)
        if self.card_in_resolution is None:
            card_in_resolution_string = ""
        else:
            card_in_resolution_string = str(self.card_in_resolution)
        result += create_tag("card_in_resolution", card_in_resolution_string)
        targets_string = "\n".join([str(target_id) for target_id in self.targets_being_selected_ids])
        result += create_tag("targets_being_selected_ids", targets_string)
        return result

    @classmethod
    def create_scene_from_string(cls, string: str):
        possible_filename, = detag_given_tags(string, "file")
        if possible_filename != "":
            file_contents = read_and_clean_file(possible_filename)
            return cls.create_scene_from_string(file_contents)
        allies_string, foes_string = detag_given_tags(string, "allies", "foes")
        actions_string, = detag_given_tags(string, "actions")
        scene = Fight_Scene(Fight_Scene.create_team_from_string(allies_string),
                            Fight_Scene.create_team_from_string(foes_string), [], [])
        list_of_action_strings = detag_repeated(actions_string, "action")
        scene.actions = [Action.create_from_string(string) for string in list_of_action_strings]
        stances_string, = detag_given_tags(string, "stances")
        list_of_stance_strings = detag_repeated(stances_string, "stance")
        scene.stances = [Stance.create_from_string(string) for string in list_of_stance_strings]

        scene._turn_side = Side[detag_given_tags(string, "turn_side")[0]]
        for person in scene.other_side:
            person.turn_ended = True
        card_in_resolution_string, targets_being_chosen_string = detag_given_tags(string, "card_in_resolution",
                                                                                  "targets_being_selected_ids")
        if card_in_resolution_string != "":
            scene.card_in_resolution = Card.create_from_string(card_in_resolution_string)
        if targets_being_chosen_string != "":
            scene.targets_being_selected_ids = [int(target_id) for target_id in targets_being_chosen_string.split("\n")]
        return scene
