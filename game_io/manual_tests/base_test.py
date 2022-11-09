import pygame as pg


def test_sprite(sprite_maker):
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1280, 700), pg.SCALED)
    sprite = sprite_maker()
    sprite.rect.center = screen.get_rect().center
    allsprites = pg.sprite.RenderPlain((sprite,))
    pg.display.set_caption("Testing")
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))
    going = True
    while going:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
        sprite.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)

        pg.display.flip()


def test_surface(surface_maker):
    def sprite_maker():
        sprite = pg.sprite.Sprite()
        sprite.image = surface_maker()
        sprite.rect = sprite.image.get_rect()
        return sprite

    test_sprite(sprite_maker)
