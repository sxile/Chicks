import pygame as pg
import numpy as np
import os
#from chicks import Chicks
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

# Image loading -- should not be here, put in new file if possible?
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


class Chick(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #super().__init__()
        self.image, self.rect = load_image("chick.png", 0)
        self.alive = True
        self.pos = ((np.random.rand() * 400) + 200, (np.random.rand() * 300) + 100)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = self.pos
        self.movedir = 7
        print(self.movedir)

    # Update Sprite, move if alive
    def update(self):
        #print("attempting update" + str(self.alive))
        if self.alive:
            if np.random.rand() < 0.01:
                self.movedir = np.random.rand() * (2 * np.pi + 5) 
                #print("attempting move")
            if self.movedir < (2 * np.pi):
                self.move()
    
    # Walk
    def move(self):
        newpos = self.rect.move((np.cos(self.movedir) * 3),np.sin(self.movedir) * 3)
        if not self.area.contains(newpos):
            if self.rect.left <= self.area.left or self.rect.right >= self.area.right:
                self.movedir = np.pi - self.movedir
                #print("reverse" + str(self.movedir))
                #self.image = pg.transform.flip(self.image, True, False)
            if self.rect.top <= self.area.top or self.rect.bottom >= self.area.bottom:
                self.movedir = 2 * np.pi - self.movedir
                #print("reverse")
            newpos = self.rect.move((np.cos(self.movedir)),np.sin(self.movedir))
        self.rect = newpos

    # Kill the chick
    def kill(self):
        self.alive = False

        #update sprite
        self.image = pg.image.load("data/dead_chick.png").convert_alpha()

    