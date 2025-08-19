import socket

from select import select

from game_logic.src.networking_constants import *
from utility.src.logging_util import server_networker_logger, server_networker_recieve_only_logger


class ServerNetworker:
    def __init__(self, HOST: str = '127.0.0.1'):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(20)
        self.connections = []
        self.receive_logging = False

    def check_for_connection(self):
        """
        Checks if someone wants to connect, connects if possible, returns None otherwise.
        :return: connection or None
        """
        if select([self.server_socket], [], [], 0.003)[0]:
            (connection, address) = self.server_socket.accept()
            self.connections.append(connection)
            return connection
        else:
            return None

    @staticmethod
    def send(message: str, connection):
        message_endcoded = message.encode(FORMAT)
        message_length = len(message_endcoded)
        message_length = str(message_length).encode(FORMAT)
        message_length += " ".encode(FORMAT) * (HEADER - len(message_length))
        connection.sendall(message_length)
        connection.sendall(message_endcoded)
        server_networker_logger.info("Message sent:\n"+message)

    def receive(self, patient=True) -> tuple:
        """
        Get *a* message.
        :return: A tuple of a sent message and the connection it is coming from.
        """
        ready_connections = select(self.connections, [], [], 0 if not patient else None)[0]
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
                server_networker_logger.info("Message recieved:\n"+data.decode(FORMAT))
                if self.receive_logging:
                    server_networker_recieve_only_logger.info("<message>"+data.decode(FORMAT)+"<\\message>")
                return data.decode(FORMAT), connection
        return "", None

    def close(self):
        self.server_socket.close()
        for connection in self.connections:
            connection.close()
