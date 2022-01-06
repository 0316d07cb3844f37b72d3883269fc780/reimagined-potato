"""
Runs all the computations.
"""
from utility.src.string_utils import detag_given_tags
from game_data.src.getter_scene import getter
class Game_Host():
    def __init__(self, fight_scene):
        self.fight_scene=fight_scene
        self.events=[]

    def add_event(self, event):
        self.check_event(event)
        self.events.append(event)

    def check_event(self,event):
        pass

    def process_event(self,event):
        if event.player.turn_ended:
            return
        if event.event_type=="PLAY_CARD":
            event.card.resolve(event.player,event.target_list)
        event.player.turn_ended=True


    def update(self):
        for event in self.events:
            self.process_event(event)
        self.events.clear()


class Event():

    def __init__(self, string):
        type, player_id = detag_given_tags(string,"type", "player_id")
        self.player=getter[int(player_id)]
        if type=="END_TURN":
            self.event_type="END_TURN"
            return self
        card_id, target_id_list=detag_given_tags(string, "card_id", "target_id_list")
        if type=="PLAY_CARD":
            self.event_type="PLAY_CARD"
            self.card=getter[int(card_id)]
            self.target_list=[getter[int(target_id)] for target_id in target_id_list]
