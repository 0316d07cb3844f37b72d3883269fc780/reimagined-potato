import unittest
from game_logic.src.client_networker import Client_Networker
from game_logic.src.server_networker import Server_Networker
from multiprocessing import Process
import time


class Test_Inits(unittest.TestCase):

    def test_initializations(self):
        my_process=Process(target=server_thread)
        my_process.start()
        time.sleep(0.01)
        client=Client_Networker()
        client.send("test")
        time.sleep(0.01)
        string=client.receive()
        self.assertEqual(string, "test")
        client.close()


def server_thread():
    server=Server_Networker()
    server.send("test")
    time.sleep(0.01)
    server.receive()
    server.close()




if __name__ == '__main__':
    unittest.main()
