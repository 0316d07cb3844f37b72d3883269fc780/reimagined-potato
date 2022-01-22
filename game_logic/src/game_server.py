import socket

from select import select

from networking_constants import *


class Game_Server():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', PORT))
        self.server_socket.listen()
        self.local_connection, self.local_address = self.server_socket.accept()

    def send(self, message: str):
        message = message.encode(FORMAT)
        message_length = len(message)
        message_length = str(message_length).encode(FORMAT)
        message_length += " ".encode(FORMAT) * (HEADER - len(message_length))
        self.local_connection.sendall(message_length)
        self.local_connection.sendall(message)

    def receive(self) -> str:
        if bool(select([self.local_connection], [], [])[0]):
            datasize = self.local_connection.recv(HEADER)
            if datasize:
                data = "".encode(FORMAT)
                datasize = int(datasize.decode(FORMAT))
                while datasize > 0:
                    data_recieved = self.local_connection.recv(datasize)
                    data += data_recieved
                    datasize -= data_recieved
                return data.decode(FORMAT)
        return ""
