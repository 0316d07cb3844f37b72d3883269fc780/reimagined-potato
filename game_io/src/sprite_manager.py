"""Takes care of the drawing of sprites and their updating."""

import pygame


class SpriteManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((1800, 800))
        # set up allsprites
        self.allsprites = pygame.sprite.RenderPlain()
        self.hand_sprites = pygame.sprite.RenderPlain()

        # make combat_background
        combat_background = pygame.Surface(self.screen.get_size())
        self.combat_background = combat_background.convert()
        self.combat_background.fill((240, 240, 240))
        self.screen.blit(combat_background, (0, 0))

    def do_frame(self):
        self.update_sprites()

    def update_sprites(self):
        self.allsprites.update()
        self.hand_sprites.update()

    def draw_new_screen(self):
        for group in (self.allsprites, self.hand_sprites):
            group.clear(self.screen, self.combat_background)
            group.draw(self.screen)
        pygame.display.flip()


