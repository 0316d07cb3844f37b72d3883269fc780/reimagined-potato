from utility.src.string_utils import *
from game_data.src.getter_scene import getter
from game_data.src.fight_scene import Fight_Scene


class ServerNetworkerWrapper:
    def __init__(self, networker):
        self.networker=networker
        self.player_to_connection = {}

    def send_to_all_players(self, string):
        for connection in self.player_to_connection.values():
            self.networker.send(string, connection)

    def get_all_messages(self):
        """
        Returns a list of tuples of messages and the scene_id of their sender.
        :return:
        """
        pass


class ClientEvent:

    def __init__(self, string):
        type, = detag_given_tags(string, "type")
        if type == "set_fightscene":
            scene_string = detag_given_tags(string, "scene")
            self.fight_scene = Fight_Scene.create_scene_from_string()
        player_id, = detag_given_tags(string, "player_id")
        self.player = getter[int(player_id)]
        if type == "END_TURN":
            self.event_type = "END_TURN"
            return
        if type == "PLAY_CARD":
            card_id, target_id_list = detag_given_tags(string, "card_id", "target_id_list")
            self.event_type = "PLAY_CARD"
            self.card = getter[int(card_id)]
            self.target_list = [getter[int(target_id)] for target_id in target_id_list]