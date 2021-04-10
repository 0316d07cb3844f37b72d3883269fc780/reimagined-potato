import pygame
import os, sys
from pygame.constants import RLEACCEL
from pygame.locals import *
from button import Button

# start pygame
pygame.init()
screen = pygame.display.set_mode((1800, 800))
clock = pygame.time.Clock()

# set up allsprites
allsprites = pygame.sprite.RenderPlain()

# set up lil sprite guy
my_sprite = pygame.sprite.Sprite()

try:
    image = pygame.image.load("resources/testguy.bmp")
except pygame.error as message:
    print("Cannot load: " + "resources/testguy.bmp")
    raise SystemExit(message)
image = image.convert()
image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
my_sprite.image, my_sprite.rect = image, image.get_rect()
my_sprite.add(allsprites)

# make background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((240, 240, 240))
screen.blit(background, (0, 0))

# make button
button_image = pygame.Surface([200, 40])
button_image.fill([100,100,70])
button_image=button_image.convert()
button_rect = button_image.get_rect()
button_rect.center=[900,500]
button_text="Beep boop"
my_Button= Button(button_text,button_image,button_rect, [lambda :print("beep booop")])
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
