import pygame
import os, sys
from pygame.constants import RLEACCEL
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1800, 800))
my_sprite = pygame.sprite.Sprite()

try:
    image = pygame.image.load("resources/testguy.bmp")
except pygame.error as message:
    print("Cannot load: " + "resources/testguy.bmp")
    raise SystemExit(message)
image = image.convert()
image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
my_sprite.image, my_sprite.rect = image, image.get_rect()
allsprites = pygame.sprite.RenderPlain(my_sprite)
allsprites.update()
clock = pygame.time.Clock()
# make background
background=pygame.Surface(screen.get_size())
background=background.convert()
background.fill((240,240,240))

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    screen.blit(background,(0,0))
    allsprites.draw(screen)
    pygame.display.flip()

pygame.quit()
