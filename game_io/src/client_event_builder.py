from game_data.src.getterscene import getter
from game_io.src.client_event import ClientEvent
from utility.src.string_utils import *


class ClientEventBuilder:
    def __init__(self):
        self.card_to_play_id = None
        self.targets = []

    def flush_state(self):
        self.card_to_play_id = None
        self.targets = []

    def undo(self):
        if self.targets:
            self.targets.pop()
        else:
            self.card_to_play_id = None

    def pass_turn(self):
        ClientEvent.trigger_event(create_tag("type", "END_TURN"))
        self.flush_state()

    def select_card_to_play(self, card_id):
        self.flush_state()
        self.card_to_play_id = card_id

    def add_target(self, target_id):
        if self.card_to_play_id is not None:
            self.targets.append(target_id)

    def finish_play_card(self):
        card = getter[self.card_to_play_id]
        if card.target_checker(self.targets):
            event = create_tag("type", "PLAY_CARD")
            event += create_tag("card_id", self.card_to_play_id)
            event += create_tag("target_id_list", self.targets)
            ClientEvent.trigger_event(event)
            self.flush_state()

    def register_card(self, card):
        def selecting_function():
            self.select_card_to_play(card.scene_id)
        card.on_click.append(selecting_function)

    def register_targetable(self, targetable):
        def selecting_funtion():
            self.add_target(targetable)
        targetable.on_click.append(selecting_funtion)


builder = ClientEventBuilder()
