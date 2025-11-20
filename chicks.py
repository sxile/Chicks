#pomodoro

import sys
import os
import pygame as pg
from chick import Chick

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    pg.display.set_caption("Pomodoro Chicks")
    pg.mouse.set_visible(True)

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    screen.blit(background, (0,0))
    pg.display.flip()

    chick = Chick()
    allsprites = pg.sprite.RenderPlain(chick)
    clock = pg.time.Clock()

    going = True

    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
        
        allsprites.update()

        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pg.display.flip()
    pg.quit()

if __name__ == "__main__":
    main()