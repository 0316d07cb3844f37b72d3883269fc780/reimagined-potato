"""
A person as it is in the Fight_Scene.
"""

from game_data.src.action import Action
from game_data.src.stance import Stance
from game_data.src.card_collection import Card_Collection, create_drawpile
from game_data.src.getterscene import getter
from game_data.src.loadable import Loadable
from game_data.src.persondata import PersonData
from game_logic.src.engine_event import EngineEvent
from utility.src.string_utils import create_tag, detag_repeated, detag_given_tags, root_path


class Person_Fighting(Loadable):
    def __init__(self, base_person: PersonData):
        self.base_person = base_person
        self.actions = []
        self.stances = []
        self.resist = 0
        self.turn_ended = False
        "Create Cardcontainers."
        self.drawpile = create_drawpile(base_person.deck)
        self.hand = Card_Collection([])
        self.discardpile = Card_Collection([])
        "Register in universal getter."
        self.scene_id = getter.register(self)

    def __str__(self):
        my_string = create_tag("base_person", str(self.base_person))
        actions_string = [str(action) for action in self.actions]
        tagged_list = [create_tag("action", string) for string in actions_string]
        my_string += create_tag("actions", ",".join(tagged_list))
        stances_string = [str(stance) for stance in self.stances]
        tagged_list = [create_tag("stance", string) for string in stances_string]
        my_string += create_tag("stances", ",".join(tagged_list))
        my_string += create_tag("resist", self.resist)
        my_string += create_tag("turn_ended", self.turn_ended)
        my_string += create_tag("drawpile", str(self.drawpile))
        my_string += create_tag("hand", str(self.hand))
        my_string += create_tag("discardpile", self.discardpile)
        my_string += create_tag("scene_id", self.scene_id)
        return my_string

    @property
    def blueprint_id(self):
        return self.base_person.person_type

    @classmethod
    def create_from_string(cls, string: str):
        possible_filename = detag_given_tags("file")
        if len(possible_filename) == 1:
            with open(root_path(*possible_filename)) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        base_person_string, = detag_given_tags(string, "base_person")
        base_person = PersonData.create_from_string(base_person_string)
        my_person_fighting = Person_Fighting(base_person)
        actions_string, = detag_given_tags(string, "actions")
        action_strings = detag_repeated(actions_string, "action")
        my_person_fighting.actions.append(
            [Action.create_from_string(action_string) for action_string in action_strings])
        stances_string, = detag_given_tags(string, "stances")
        stance_strings = detag_repeated(stances_string, "stance")
        my_person_fighting.stances.append(
            [Stance.create_from_string(stance_string) for stance_string in stance_strings])
        resist, turn_ended = detag_given_tags(string, "resist", "turn_ended")
        if (resist, turn_ended) != ("", ""):
            my_person_fighting.resist, my_person_fighting.turn_ended = int(resist), bool(turn_ended)
        drawpile_string, hand_string, discardpile_string = detag_given_tags(string, "drawpile", "hand", "discardpile")
        my_person_fighting.drawpile = Card_Collection.create_from_string(drawpile_string)
        my_person_fighting.hand = Card_Collection.create_from_string(hand_string)
        my_person_fighting.discardpile = Card_Collection.create_from_string(discardpile_string)
        id_string, = detag_given_tags(string, "scene_id")
        getter[int(id_string)] = my_person_fighting
        return my_person_fighting

    @classmethod
    def load_from_file(cls, card_name: str):

        with open("/../../resources/cards/" + card_name, 'r') as file:
            return cls.create_from_string(file.read())

    def damage(self, damage):
        if damage > self.resist:
            self.base_person.damage(damage - self.resist)
            self.resist = 0
        else:
            self.resist -= max(damage, 0)

    def play_card(self, card, target_list):
        """
        Plays a card from hand.
        :param card: The card to be played.
        :param target_list: Possibly empty list of targets.
        :return:
        """
        if card not in self.hand:
            raise IndexError("Card not in Hand can't be played.")
        card.resolve(self, target_list)
        card.move(self.discardpile)

    def draw_card(self):
        if len(self.drawpile) != 0:
            card = self.drawpile.get_a_card()
            card.move(self.hand)
        elif len(self.discardpile) != 0:
            self.shuffle_discardpile_into_drawpile()
            self.draw_card()

    def shuffle_discardpile_into_drawpile(self):
        for card in self.discardpile.get_all_cards():
            card.move(self.drawpile)
        self.drawpile.shuffle()

    def get_health(self):
        return self.base_person.health

    def append_action(self, action):
        self.actions.append(action)

    def die(self):
        pass

    def has_stance(self) -> bool:
        pass
