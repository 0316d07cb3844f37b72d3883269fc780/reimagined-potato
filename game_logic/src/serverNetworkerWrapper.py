from game_data.src.fight_scene import Fight_Scene
from game_data.src.getterscene import getter
from game_logic.src.servernetworker import ServerNetworker
from utility.src.string_utils import *


class ServerNetworkerWrapper:
    def __init__(self, networker: ServerNetworker):
        self.networker = networker
        self.player_to_connection = {}

    def send_to_all_players(self, string):
        outdated_connections = []
        for connection in self.player_to_connection.values():
            try:
                self.networker.send(string, connection)
            except ConnectionError:
                for player, other_connection in self.player_to_connection.items():
                    if connection == other_connection:
                        outdated_connections.append(player)
        for player in outdated_connections:
            del self.player_to_connection[player]

    def get_all_messages(self):
        """
        Returns ClientEvents
        :return: List of ClientEvents
        """
        return self.__get_all_messages_internal()

    def __get_all_messages_internal(self, subresult: list = None):
        if subresult is None:
            subresult = []
        while self.networker.check_for_connection() is not None:
            pass

        string, connection = self.networker.receive(not subresult)

        if connection is not None:
            try:
                my_event = ClientEvent(string)
            except Exception as exception:
                raise exception
            if my_event.event_type == "Introduction":
                self.player_to_connection[my_event.person_id] = connection
            else:
                subresult.append(my_event)
            return self.__get_all_messages_internal(subresult=subresult)
        return subresult


class MockPassWrapper:
    def __init__(self, engine):
        self.server = engine
        self.result = []

    def send_to_all_players(self, string):
        pass

    def get_all_messages(self):
        """
        Returns ClientEvents
        :return: List of ClientEvents
        """
        if self.result:
            result = [self.result]
        else:
            result = []
            for person in self.server.scene.current_side:
                result.append(ClientEvent.create_end_turn_generating_string(person.scene_id))
        self.result = []
        return result

    def set_next_messages(self, messages):
        self.result = messages


class ClientEvent:

    def __init__(self, string):
        self.event_type, = detag_given_tags(string, "type")
        if self.event_type in ["END_ENGINE", "START_SCENE", "ACCEPT_CONNECTION"]:
            return
        if self.event_type == "Introduction":
            self.person_id = int(*detag_given_tags(string, "person_id"))
            return
        if self.event_type == "set_fightscene":
            scene_string, = detag_given_tags(string, "scene")
            self.fight_scene = Fight_Scene.create_scene_from_string(scene_string)
            return
        player_id, = detag_given_tags(string, "player_id")
        self.player = getter[int(player_id)]
        if self.event_type == "END_TURN":
            pass
        if self.event_type == "PLAY_CARD":
            card_id, target_id_list_string = detag_given_tags(string, "card_id", "target_id_list")
            target_id_list = eval(target_id_list_string)
            self.card = getter[int(card_id)]
            self.target_list = [getter[target_id] for target_id in target_id_list]

    @classmethod
    def create_end_turn_generating_string(cls, player_id: int):
        generating_string = create_tag("type", "END_TURN")
        generating_string += create_tag("player_id", player_id)
        return generating_string

    @classmethod
    def create_play_card_generating_string(cls, player_id: int, card_id: int, target_id_list: int):
        generating_string = create_tag("type", "PLAY_CARD")
        generating_string += create_tag("player_id", player_id)
        generating_string += create_tag("card_id", card_id)
        generating_string += create_tag("target_id_list", target_id_list)
        return generating_string
