"""
An action that a person will perform at the end of the turn.
"""

from itertools import product

from game_data.src.atomic_event import *
from game_data.src.getterscene import getter
from game_data.src.loadable import Loadable


class Speed(Enum):
    Channel = 0
    Regular = 1
    Fast = 2
    Instant = 3


class Action(Loadable):
    def __init__(self, name: str, performer, target_list: list, method: callable, speed: Speed, stability: int,
                 action_id: int):
        self.name = name
        self.performer = performer
        self.target_list = target_list
        self.method = method
        self.speed = speed
        self.stability = stability
        self.action_id = action_id
        self.scene_id = getter.register(self)
        performer.append_action(self)

    def __str__(self) -> str:
        my_string = create_tag("name", self.name)
        my_string += create_tag("performer_id", self.performer.scene_id)
        my_string += create_tag("target_id_list", [target.scene_id for target in self.target_list])
        my_string += create_tag("speed", self.speed.name)
        my_string += create_tag("stability", self.stability)
        my_string += create_tag("action_id", self.action_id)
        my_string += create_tag("scene_id", self.scene_id)
        return my_string

    @classmethod
    def create_from_string(cls, string: str):
        possible_filename = detag_given_tags("file")
        if len(possible_filename) == 1:
            with open(root_path(*possible_filename)) as file:
                file_contents = file.read()
            return cls.create_from_string(file_contents)
        tags = "name", "performer_id", "target_id_list", "stability", "action_id", "scene_id"
        name, performer_id, target_id_list, stability, action_id, scene_id = detag_given_tags(string, *tags)
        target_id_list = get_id_list(target_id_list)
        performer_id = int(performer_id)
        action_id = int(action_id)
        target_list = [getter[target_id] for target_id in target_id_list]
        action = creator_by_id[action_id](getter[performer_id], target_list)
        action.stability = stability
        getter[int(scene_id)] = action
        return action

    @property
    def blueprint_id(self):
        return self.action_id

    def resolve(self) -> None:
        self.method(self.performer.scene_id, *self.target_list)
        self.performer.actions.remove(self)

    def damage(self, damage_amount):
        self.stability -= max(damage_amount, 0)

    def get_destroyed(self):
        del self


def create_stunned(stunned_guy) -> Action:
    return Action("Stunned", stunned_guy, [], lambda: None, Speed.Regular, 3, 0)


def tackle_method(_, *tackled):
    return [damage(tackled, 6)]


def create_tackle(tackler, tackled_list: list) -> Action:
    tackle = Action("Tackle", tackler, tackled_list, tackle_method, Speed.Fast, 3, 1)
    return tackle


def brace_method(bracer, _):
    return [add_resist(bracer, 5)]


def create_brace(bracer, braced=None) -> Action:
    return Action("Brace", bracer, [], brace_method, Speed.Instant, 2, 2)


def side_step_method(stepper, stepped_action):
    return [AtomicEvent(EventType.untarget, action=stepped_action, targeted=stepper)]


def create_side_step(stepper, to_be_stepped):
    return Action("Sidestep", stepper, [to_be_stepped], side_step_method, Speed.Fast, 3, 3)


def crushing_blow_method(_, to_be_crushed_person):
    return [damage(to_be_crushed_person, 10)]


def create_crushing_blow(crusher, crushed):
    return Action("Crushing Blow", crusher, [crushed], crushing_blow_method, Speed.Regular, 5, 4)


def tail_swipe_method(_, to_be_swiped_action):
    return [destroy(to_be_swiped_action)]


def create_tail_swipe(swiper, to_be_swiped_action):
    return Action("Tail Swipe", swiper, [to_be_swiped_action], tail_swipe_method, Speed.Fast, 3, 5)


def reckless_assault_method(assaulter, assaulted):
    return [damage(assaulter, 3), damage(assaulted, 12)]


def create_reckless_assault(assaulter, assaulted):
    return Action("Reckless Assault", assaulter, [assaulted], reckless_assault_method, Speed.Regular, 5, 6)


def bark_skin_blessing_method(they_who_blesses, blessed):
    return add_resist(they_who_blesses, 3), add_resist(blessed, 10)


def create_bark_skin_blessing(they_who_blesses, blessed):
    return Action("Bark Skin Blessing", they_who_blesses, [blessed], bark_skin_blessing_method, Speed.Instant, 1, 7)


def engulf_in_flames_method(they_who_engulf, engulfeds):
    return [damage(engulfed, 3) for _, engulfed in product(range(5), engulfeds)]


def create_engulf_in_flames(they_who_engulf, engulfed):
    return Action("Engulf in Flames", they_who_engulf, [engulfed], engulf_in_flames_method, Speed.Channel, 4, 8)


def sunshine_blessing_method(they_who_blesses, blessed_action):
    return add_stability(blessed_action, 10),


def create_sunshine_blessing(they_who_blesses, blessed_action):
    return Action("Sunshine Blessing", they_who_blesses, [blessed_action], sunshine_blessing_method, Speed.Instant, 2,
                  9)


def mind_blast_method(blaster, blasted):
    return damage(blasted, 3),


def create_mind_blast(blaster, blasted):
    return Action("Mind Blast", blaster, [blasted], mind_blast_method, Speed.Instant, 1, 10)


def inspiration_method(inspired, _):
    return AtomicEvent(EventType.draw_card, drawer=inspired), *2


creator_by_id = {
    0: create_stunned,
    1: create_tackle,
    2: create_brace,
    3: create_side_step,
    4: create_crushing_blow,
    5: create_tail_swipe,
    6: create_reckless_assault,
    7: create_bark_skin_blessing,
    8: create_engulf_in_flames,
    9: create_sunshine_blessing,
    10: create_mind_blast,

}
