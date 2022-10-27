import socket

from select import select

from game_logic.src.networking_constants import *


class ServerNetworker:
    def __init__(self, HOST: str = '127.0.0.1'):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(20)
        self.connections = []

    def check_for_connection(self):
        if select([self.server_socket], [], [], 0.005)[0]:
            (connection, address) = self.server_socket.accept()
            self.connections.append(connection)
            return connection
        else:
            return None

    def send(self, message: str, connection):
        message = message.encode(FORMAT)
        message_length = len(message)
        message_length = str(message_length).encode(FORMAT)
        message_length += " ".encode(FORMAT) * (HEADER - len(message_length))
        connection.sendall(message_length)
        connection.sendall(message)

    def receive(self) -> tuple:
        """
        :return: A tuple of a sent message and the connection it is coming from.
        """
        ready_connections = select(self.connections, [], [])[0]
        if ready_connections:
            connection = ready_connections.pop()
            datasize = connection.recv(HEADER)
            if datasize:
                data = "".encode(FORMAT)
                datasize = int(datasize.decode(FORMAT))
                while datasize > 0:
                    data_recieved = connection.recv(datasize)
                    data += data_recieved
                    datasize -= len(data_recieved)
                return data.decode(FORMAT), connection
        return "", None

    def close(self):
        self.server_socket.close()
        for connection in self.connections:
            connection.close()
