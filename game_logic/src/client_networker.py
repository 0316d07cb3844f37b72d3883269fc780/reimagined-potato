import socket
from socket import socket

from select import select

from networking_constants import *


class Client_Networker():
    _socket: socket

    def __init__(self, Host, Socket=None):
        if Socket == None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((Host, PORT))

    def send(self, message: str):
        message = message.encode(FORMAT)
        message_length = len(message)
        message_length = str(message_length).encode(FORMAT)
        message_length += " ".encode(FORMAT) * (HEADER - len(message_length))
        self._socket.sendall(message_length)
        self._socket.sendall(message)

    def receive(self) -> str:
        if select([self._socket], [], []):
            data_size = self._socket.recv(HEADER)
            if data_size:
                data = "".encode(FORMAT)
                data_size = int(data_size.decode(FORMAT))
                while data_size > 0:
                    data_recieved = self._socket.recv(data_size)
                    data += data_recieved
                    data_size -= data_recieved
                return data.decode(FORMAT)
        return ""


if __name__ == "__main__":
    pass
