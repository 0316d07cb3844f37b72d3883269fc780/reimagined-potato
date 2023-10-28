import pygame
from pygame.locals import *
from game_io.src.button import Button
from game_io.src.image_util import stack_vertical
from game_logic.src.client_networker import Client_Networker
from game_io.src.client_event import ClientEvent
from game_io.src.scene_aranger import *
from game_io.src.sprite_manager import SpriteManager


def main():
    # start pygame
    pygame.init()
    sprite_manager = SpriteManager()
    networker = Client_Networker()

    scene = None

    initialize_scene(scene, 0, sprite_manager.allsprites, sprite_manager.hand_sprites)

    # gameloop
    client_loop(sprite_manager, networker)


def client_loop(sprite_manager: SpriteManager, networker):
    clock = pygame.time.Clock()
    running = True
    while running:
        engine_events = get_engine_events(networker)
        clock.tick(60)
        handle_engine_events(engine_events)
        sprite_manager.do_frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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


def button_test(allsprites):
    button_image = pygame.Surface([200, 40])
    button_image.fill([140, 140, 120])
    button_image = button_image.convert()
    button_rect = button_image.get_rect()
    button_rect.center = [900, 500]
    button_text = "Beep boop"
    button_images = [button_image, button_image.copy(), button_image.copy()]
    button_images[1].fill([120, 120, 105])
    button_images[2].fill([100, 100, 90])
    my_Button = Button(button_images, button_rect, button_text, [lambda: print("beep booop")])
    my_Button.add(allsprites)


def guy_test(allsprites):
    my_sprite = pygame.sprite.Sprite()
    try:
        image = pygame.image.load("resources/Testguy.bmp")
    except pygame.error as message:
        print("Cannot load: " + "resources/testguy.bmp")
        raise SystemExit(message)
    image = image.convert()
    image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
    image = stack_vertical(image, image)
    my_sprite.image, my_sprite.rect = image, image.get_rect()
    my_sprite.add(allsprites)


if __name__ == "__main__":
    main()
