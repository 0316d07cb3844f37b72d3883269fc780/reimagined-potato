"""
Runs all the computations.
"""
from utility.src.string_utils import detag_given_tags
from game_data.src.getter_scene import getter
class Combat_Engine():
    def __init__(self, fight_scene):
        self.fight_scene=fight_scene


    def process_event(self,event):
        if event.player.turn_ended:
            return
        if event.event_type=="PLAY_CARD":
            event.card.resolve(event.player,event.target_list)
        event.player.turn_ended=True
        self.check_if_turn_over()

    def check_if_turn_over(self):
        if all([person.turn_ended for person in self.fight_scene.current_side]):
            self.fight_scene.change_turn()




class Event():

    def __init__(self, string):
        type, player_id = detag_given_tags(string,"type", "player_id")
        self.player=getter[int(player_id)]
        if type=="END_TURN":
            self.event_type="END_TURN"
            return
        card_id, target_id_list=detag_given_tags(string, "card_id", "target_id_list")
        if type=="PLAY_CARD":
            self.event_type="PLAY_CARD"
            self.card=getter[int(card_id)]
            self.target_list=[getter[int(target_id)] for target_id in target_id_list]
