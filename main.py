from multiprocessing import Process, Event

import pygame

from ai.src.ai import ai_loop
from game_data.src.fight_scene import Fight_Scene
from game_data.src.getterscene import getter
from game_io.src.client_event import ClientEvent
from game_io.src.client_event_builder import builder
from game_io.src.scene_aranger import render_event_pre, render_event_post, initialize_scene
from game_io.src.sprite_manager import SpriteManager
from game_logic.src.client_networker import Client_Networker, get_engine_events
from game_logic.src.combatengine import CombatEngine
from game_logic.src.scene_transformer import transform
from game_logic.src.serverNetworkerWrapper import ServerNetworkerWrapper
from game_logic.src.servernetworker import ServerNetworker
from utility.src.string_utils import create_tag


def main():
    # start pygame
    pygame.init()
    sprite_manager = SpriteManager()
    scene = Fight_Scene.create_scene_from_string("<file>resources/Scenes/two_dogs_fighting.scene<\\file>")
    engine_runs = Event()
    engine_process = Process(target=engine_loop,
                             args=("<file>resources/Scenes/two_dogs_fighting.scene<\\file>", engine_runs))
    engine_process.start()
    engine_runs.wait()
    ai_process = Process(target=ai_loop,
                         args=("<file>resources/Scenes/two_dogs_fighting.scene<\\file>", scene.foes[0].scene_id))
    ai_process.start()
    client_networker = Client_Networker()
    index_player = 0
    builder.player_id = scene.allies[index_player].scene_id

    initialize_scene(scene, index_player, sprite_manager.allsprites, sprite_manager.hand_sprites)
    client_networker.introduce_self(index_player)
    client_networker.send(create_tag("type", "START_SCENE"))
    client_networker.send(create_tag("type", "ACCEPT_CONNECTION"))

    # gameloop
    client_loop(sprite_manager, client_networker, engine_process, scene, index_player)
    ai_process.terminate()


def client_loop(sprite_manager: SpriteManager, networker, engine_process, scene, index_player):
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        engine_events = get_engine_events(networker)
        handle_engine_events(engine_events, scene, index_player, sprite_manager)
        sprite_manager.do_frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                networker.stop_engine()
                engine_process.join()
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                builder.pass_priority()

        for event in ClientEvent.get_and_flush_events():
            networker.send(event)

    pygame.quit()


def handle_engine_events(events, scene, index_player, sprite_manager):
    for event in events:
        render_event_pre(scene, event, index_player, sprite_manager.allsprites, sprite_manager.hand_sprites)
        transform(event, getter, scene)
        render_event_post(scene, event, index_player, sprite_manager.allsprites, sprite_manager.hand_sprites)


def engine_loop(scene_string, engine_runs):
    server_networker = ServerNetworker()
    server_networker.activate_logging()
    server_network_wrapper = ServerNetworkerWrapper(server_networker)
    combat_engine = CombatEngine(server_network_wrapper, Fight_Scene.create_scene_from_string(scene_string))
    engine_runs.set()
    combat_engine.engine_loop()


def let_engine_start_scene(networker):
    start_message = create_tag("type", "START_SCENE")
    networker.send(start_message)


if __name__ == "__main__":
    main()
