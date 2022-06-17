from game_logic.src.server_networker import Server_Networker
from game_logic.src.combat_engine import Combat_Engine, Event

def start_server():
    networker = Server_Networker()
    engine=Combat_Engine()
    server_loop(networker, engine)

def server_loop(networker, engine):
    while True:
        command = networker.receive()
        if command == "Shutdown":
            break
        event = Event(command)
        engine.process_event()