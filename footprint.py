import pygame as pg
import numpy as np
# import os
from spritesheet import SpriteSheet

class Footprint():
    def __init__(self, dir, coord):
        footprints_spritesheet_img = pg.image.load('data/footprints.png')
        footprints_spritesheet = SpriteSheet(footprints_spritesheet_img)
        self.footprint = footprints_spritesheet.get_image(dir, 10, 10, 4)

        self.coord = coord

    def draw(self, screen):
        screen.blit(self.footprint, self.coord)
