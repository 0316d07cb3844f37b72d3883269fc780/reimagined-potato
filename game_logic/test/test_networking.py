import time
import unittest
from multiprocessing import Process

from game_logic.src.client_networker import Client_Networker
from game_logic.src.servernetworker import ServerNetworker


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
        self.assertEqual(string, "success")
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


if __name__ == '__main__':
    unittest.main()
