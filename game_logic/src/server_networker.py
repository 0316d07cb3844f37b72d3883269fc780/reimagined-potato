import socket

from select import select

from game_logic.src.networking_constants import *


class Server_Networker():
    def __init__(self, HOST : str = '127.0.0.1'):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        (connection, address) = self.server_socket.accept()
        self.local_connection, self.local_adress=connection,address


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
                    datasize -= len(data_recieved)
                return data.decode(FORMAT)
        return ""

    def close(self):
        self.server_socket.close()
        self.local_connection.close()
