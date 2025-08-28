import socket

from select import select

from game_data.src.atomic_event import AtomicEvent
from game_logic.src.networking_constants import *
from utility.src.string_utils import create_tag, detag_repeated, root_path
from utility.src.logging_util import client_networker_logger, client_networker_recieve_only_logger


class Client_Networker:
    _socket: socket

    def __init__(self, HOST : str = '127.0.0.1', Socket=None, patient: bool = False, log_recieve_seperately: bool = False):
        if Socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((HOST, PORT))
        self.patient = patient
        self.log_recieve_seperately = log_recieve_seperately

    def send(self, message: str):
        client_networker_logger.info("Message sent:\n"+message)
        message = message.encode(FORMAT)
        message_length = len(message)
        message_length = str(message_length).encode(FORMAT)
        message_length += " ".encode(FORMAT) * (HEADER - len(message_length))
        self._socket.sendall(message_length)
        self._socket.sendall(message)

    def receive(self, impatient_mode: bool = False) -> str:
        if self.select(impatient_mode):
            data_size = self._socket.recv(HEADER)
            if data_size:
                data = "".encode(FORMAT)
                data_size = int(data_size.decode(FORMAT))
                while data_size > 0:
                    data_recieved = self._socket.recv(data_size)
                    data += data_recieved
                    data_size -= len(data_recieved)
                client_networker_logger.info("Message recieved:\n"+data.decode(FORMAT))
                if self.log_recieve_seperately:
                    client_networker_recieve_only_logger.info(create_tag("message", data.decode(FORMAT)))
                return data.decode(FORMAT)
        return ""

    def select(self, impatient_mode: bool = False):
        if self.patient and not impatient_mode:
            return select([self._socket], [], [])[0]
        else:
            return select([self._socket], [], [], 0.005)[0]

    def close(self):
        self._socket.close()

    def stop_engine(self):
        end_message = create_tag("type", "END_ENGINE")
        self.send(end_message)

    def introduce_self(self, index: int):
        """
        Introduce self to the engine, so you get sent recieved_messages

        :param index: Index of the player in Allies in the scene.
        """
        message = create_tag("type", "Introduction")
        message += create_tag("person_id", index)
        self.send(message)


class MockNetworker(Client_Networker):
    def __init__(self, messages: list = None, message_string: str = None, message_file: str = None):
        if messages is not None:
            self.recieved_messages = messages
        elif message_string is not None:
            self.recieved_messages = detag_repeated(message_string, "message")
        elif message_file is not None:
            with open(root_path(message_file), "r") as file:
                self.recieved_messages = detag_repeated(file.read(), "message")
        else:
            self.recieved_messages = []
        self.sent_messages = []

    def send(self, message: str):
        self.sent_messages.append(message)

    def receive(self, impatient_mode: bool = False):
        if self.recieved_messages:
            return self.recieved_messages.pop(0)
        return ""


    def close(self):
        pass





if __name__ == "__main__":
    pass


def get_engine_events(networker: Client_Networker):
    events = networker.receive()
    result = []
    while events != "":
        result += detag_repeated(events, "event")
        events = networker.receive(impatient_mode=True)
    result = [AtomicEvent.create_from_string(event) for event in result]
    return result
