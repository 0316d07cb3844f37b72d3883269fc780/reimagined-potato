import pygame
from pygame.locals import *
from game_io.src.button import Button
from game_io.src.image_util import stack_vertical
from game_logic.src.client_networker import Client_Networker
from game_logic.src.servernetworker import ServerNetworker
from game_logic.src.serverNetworkerWrapper import ServerNetworkerWrapper
from game_logic.src.combatengine import CombatEngine
from game_io.src.client_event import ClientEvent
from game_io.src.scene_aranger import *
from game_io.src.sprite_manager import SpriteManager
from utility.src.string_utils import create_tag
from multiprocessing import Process, Event


def main():
    # start pygame
    pygame.init()
    sprite_manager = SpriteManager()
    scene = Fight_Scene.create_scene_from_string("<file>resources/Scenes/two_dogs_fighting.scene<\\file>")
    engine_runs = Event()
    engine_process = Process(target=engine_loop, args=("<file>resources/Scenes/two_dogs_fighting.scene<\\file>", engine_runs))
    engine_process.start()
    engine_runs.wait()
    client_networker = Client_Networker()

    initialize_scene(scene, 0, sprite_manager.allsprites, sprite_manager.hand_sprites)

    # gameloop
    client_loop(sprite_manager, client_networker, engine_process)


def client_loop(sprite_manager: SpriteManager, networker, engine_process):
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        engine_events = get_engine_events(networker)
        handle_engine_events(engine_events)
        sprite_manager.do_frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                networker.stop_engine()
                engine_process.join()
                running = False
        for event in ClientEvent.get_and_flush_events():
            networker.send(event)

    pygame.quit()


def get_engine_events(networker: Client_Networker):
    event = networker.receive()
    result = []
    while event != "":
        result += event
        event = networker.receive()
    return result


def handle_engine_events(events):
    for event in events:
        pass


def engine_loop(scene_string, engine_runs):
    server_networker = ServerNetworker()
    server_network_wrapper = ServerNetworkerWrapper(server_networker)
    combat_engine = CombatEngine(server_network_wrapper, Fight_Scene.create_scene_from_string(scene_string))
    engine_runs.set()
    combat_engine.engine_loop()


def let_engine_start_scene(networker):
    start_message = create_tag("type", "START_SCENE")
    networker.send(start_message)


if __name__ == "__main__":
    main()
