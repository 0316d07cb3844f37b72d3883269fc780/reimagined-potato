from game_logic.src.server_networker import Server_Networker
from game_logic.src.combatengine import CombatEngine, ClientEvent
from game_logic.src.engine_event import EngineEvent


def start_server():
    networker = Server_Networker()
    engine = CombatEngine()
    server_loop(networker, engine)


def server_loop(networker, engine):
    while True:
        command = networker.receive()
        if command == "Shutdown":
            break
        client_event = ClientEvent(command)
        engine.process_event(client_event)
        engine_events = EngineEvent.get_and_flush_events()
        for event in engine_events:
            networker.send(event)
