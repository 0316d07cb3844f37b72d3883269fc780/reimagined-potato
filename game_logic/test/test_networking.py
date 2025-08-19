import time
import unittest
from multiprocessing import Process

from game_logic.src.client_networker import Client_Networker
from game_logic.src.servernetworker import ServerNetworker
from utility.src.string_utils import create_tag
from utility.src.logging_util import clear_all_files


class TestInits(unittest.TestCase):

    def test_sending_and_recieving(self):
        my_process = Process(target=server_thread)
        my_process.start()
        client = Client_Networker()
        client.send("test")
        for _ in range(60):
            client.send("test")
        string = client.receive()
        self.assertEqual(string, "test")
        empty = client.receive()
        self.assertEqual(empty, "")
        my_process.join()
        client.close()

    def test_server_waits_for_client(self):
        my_process = Process(target=patient_server)
        my_process.start()
        client = Client_Networker()
        client.send("test")
        string = client.receive()
        self.assertEqual("success", string)
        my_process.join()
        client.close()

    def test_client_doesnt_wait_to_recieve(self):
        my_process = Process(target=patient_server)
        my_process.start()
        client = Client_Networker()
        client.receive()
        client.send("done")
        my_process.join()
        client.close()

    def test_patient_client(self):
        my_process = Process(target=delayed_server)
        my_process.start()
        client = Client_Networker(patient=True)
        string = client.receive()
        self.assertEqual(string, "message")
        my_process.join()
        client.close()

    def test_two_clients(self):
        server_process = Process(target=server_thread_two_servers)
        server_process.start()
        client_process = Process(target=first_client_two_clients)
        client_process.start()
        second_client_two_clients(self)
        server_process.join()
        client_process.join()

    def test_server_networker_mock(self):
        clear_all_files()
        server = ServerNetworker()
        server.receive_logging = True
        connection = None
        client_process = Process(target=client_thread_logging)
        client_process.start()
        while connection is None:
            connection = server.check_for_connection()
        string, _ = server.receive()
        server.close()
        client_process.join()


def client_thread_logging():
    client = Client_Networker()
    to_send_string = create_tag("type", "START_SCENE")
    client.send(to_send_string)
    client.close()


def server_thread():
    server = ServerNetworker()
    connection = None
    while connection is None:
        connection = server.check_for_connection()
    server.send("test", connection)
    time.sleep(0.01)
    server.receive()
    for _ in range(60):
        server.receive()
    server.close()


def server_thread_logging():
    server = ServerNetworker()
    server.receive_logging = True
    connection = None
    while connection is None:
        connection = server.check_for_connection()
    server.receive()
    server.close()


def patient_server():
    server = ServerNetworker()
    connection = None
    while connection is None:
        connection = server.check_for_connection()
    string, _ = server.receive()
    if string == "test":
        server.send("success", connection)
    else:
        server.send("failure", connection)
    server.close()


def silent_server():
    server = ServerNetworker()
    connection = None
    while connection is None:
        connection = server.check_for_connection()
    server.receive()
    server.close()


def delayed_server():
    server = ServerNetworker()
    connection = None
    while connection is None:
        connection = server.check_for_connection()
    time.sleep(0.1)
    server.send("message", connection)
    server.close()


def server_thread_two_servers():
    server = ServerNetworker()
    connection_1, connection_2 = None, None
    while connection_1 is None:
        connection_1 = server.check_for_connection()
    while connection_2 is None:
        connection_2 = server.check_for_connection()
    time.sleep(0.01)
    string, _ = server.receive()
    if string == "first_string":
        server.send("test", connection_1)
        server.send("test", connection_2)
    string, _ = server.receive()
    if string == "done":
        server.send("done", connection_1)
    server.close()


def first_client_two_clients():
    time.sleep(0.01)
    client = Client_Networker()
    client.send("first_string")
    while client.receive() != "done":
        time.sleep(0.04)
    client.close()


def second_client_two_clients(self):
    time.sleep(0.01)
    second_client = Client_Networker(patient=True)
    received_string = second_client.receive()
    self.assertEqual(received_string, "test")
    second_client.send("done")
    second_client.close()


if __name__ == '__main__':
    unittest.main()
