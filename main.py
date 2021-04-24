import pygame
import game_data
import game_logic
import game_io
from pygame.locals import *
from game_io.button import Button
from game_io.image_util import stack_vertical


def main():
    # start pygame
    pygame.init()
    screen = pygame.display.set_mode((1800, 800))
    clock = pygame.time.Clock()
    # set up allsprites
    allsprites = pygame.sprite.RenderPlain()

    # set up lil sprite guy
    #guy_test(allsprites)

    # make background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((240, 240, 240))
    screen.blit(background, (0, 0))
    # make button
    button_image = pygame.Surface([200, 40])
    button_image.fill([140, 140, 120])
    button_image = button_image.convert()
    button_rect = button_image.get_rect()
    button_rect.center = [900, 500]
    button_text = "Beep boop"
    button_images = [button_image, button_image.copy(), button_image.copy()]
    button_images[1].fill([120, 120, 105])
    button_images[2].fill([100, 100, 90])
    my_Button = Button(button_text, button_images, button_rect, [lambda: print("beep booop")])
    my_Button.add(allsprites)
    running = True
    while running:
        clock.tick(60)
        # update game logic
        allsprites.update()
        # draw new screen
        allsprites.clear(screen, background)
        allsprites.draw(screen)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
    pygame.quit()


def guy_test(allsprites):
    my_sprite = pygame.sprite.Sprite()
    try:
        image = pygame.image.load("resources/testguy.bmp")
    except pygame.error as message:
        print("Cannot load: " + "resources/testguy.bmp")
        raise SystemExit(message)
    image = image.convert()
    image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
    image = stack_vertical([image, image])
    my_sprite.image, my_sprite.rect = image, image.get_rect()
    my_sprite.add(allsprites)


main()
