from game_logic.src.servernetworker import ServerNetworker
from game_logic.src.combatengine import CombatEngine, ClientEvent
from game_logic.src.engine_event import EngineEvent


def start_server():
    networker = ServerNetworker()
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
