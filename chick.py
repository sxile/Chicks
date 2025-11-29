import pygame as pg
import numpy as np
import os
from spritesheet import SpriteSheet
#from chicks import Chicks
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

#BLACK = (0,0,0)

class Chick(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        # Resources (spritesheets, timers)
        self.animation_timer = pg.time.get_ticks() + (np.random.rand() * 1000)
        
        standing_spritesheet_image = pg.image.load('data/chick_standing.png').convert_alpha()
        walking_spritesheet_image = pg.image.load('data/chick_walking.png').convert_alpha()
        death_spritesheet_image = pg.image.load('data/chick_death.png').convert_alpha()
        
        standing_spritesheet = SpriteSheet(standing_spritesheet_image)
        walking_spritesheet = SpriteSheet(walking_spritesheet_image)
        death_spritesheet = SpriteSheet(death_spritesheet_image)

        self.standing_frames = [None,None]
        self.walking_frames = [None,None,None,None,None,None]
        self.death_frames = [None,None,None,None,None,None,
                        None,None,None,None,None,None,
                        None,None,None,None,None,None,
                        None]


        self.standing_frames = [standing_spritesheet.get_image(0, 25, 28, 4),standing_spritesheet.get_image(1, 25, 28, 4)]
        for i in range(6):
            self.walking_frames[i] = walking_spritesheet.get_image(i, 25, 28, 4)

        for i in range(19):
            self.death_frames[i] = death_spritesheet.get_image(i, 25, 28, 4)


        # Initialization
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.alive = True
        self.pos = ((np.random.rand() * 400) + 200, (np.random.rand() * 300) + 100)
        self.screen = pg.display.get_surface()
        self.area = self.screen.get_rect()
        self.rect.topleft = self.pos
        self.movedir = 7
        #print(self.movedir)

    # Update Sprite, move if alive
    def update(self):
        #print("attempting update" + str(self.alive))
        if self.alive:
            if np.random.rand() < 0.01:
                self.movedir = np.random.rand() * (2 * np.pi + 5) 
                #print("new direction!")
            if self.movedir < (2 * np.pi):
                self.move()
                #trying to move!
            else:
                # Blinking / Standing timer
                if (self.animation_timer - pg.time.get_ticks()) % 1000 > 890:
                    self.image = self.standing_frames[1]
                else:
                    self.image = self.standing_frames[0]
        else:
            frame = int((pg.time.get_ticks() - self.animation_timer) / 50)

            # Death Animation
            if frame >= 0 and frame < 19:
                #print(frame)
                self.image = self.death_frames[frame]
            elif frame < 0:
                self.image = self.standing_frames[0]
            else:
                self.image = self.death_frames[18]

    
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
        #print("trying to walk!")
        self.image = self.walking_frames[int(((self.animation_timer - pg.time.get_ticks()) % 1000) / 167)]

    # Kill the chick
    def kill(self):
        if not self.alive:
            return False
        else:
            self.image = self.standing_frames[0]
            self.animation_timer = pg.time.get_ticks() + 2000
            self.alive = False
            return True
    