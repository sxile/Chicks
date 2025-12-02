import pygame as pg
import numpy as np
# import os
from spritesheet import SpriteSheet
from footprint import Footprint
#from chicks import Chicks
# main_dir = os.path.split(os.path.abspath(__file__))[0]
# data_dir = os.path.join(main_dir, "data")

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
        self.inBlood = False
        self.footprints = []
        self.left_last_footprint = pg.time.get_ticks()
        self.walked_through_blood = 0
        #print(self.movedir)

    # Update Sprite, move if alive
    def update(self, screen):
        for fprint in self.footprints:
            fprint.draw(screen)
        #print("attempting update" + str(self.alive))
        if self.alive:
            if pg.time.get_ticks() - self.walked_through_blood > 10000:
                self.inBlood = False
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

    def standingInBlood(self):
        if self.alive:
            # if not self.inBlood:
            #     print("stepped in blood")
            self.inBlood = True
            self.walked_through_blood = pg.time.get_ticks()
    
    # Walk
    def move(self):
        newpos = self.rect.move((np.cos(self.movedir) * 3),0 - (np.sin(self.movedir) * 3))
        if not self.area.contains(newpos):
            if self.rect.left <= self.area.left + 5 or self.rect.right >= self.area.right - 5:
                self.movedir = np.pi - self.movedir
                self.movedir = self.movedir % (2 * np.pi)
                #print("reverse" + str(self.movedir))
                #self.image = pg.transform.flip(self.image, True, False)
            if self.rect.top <= self.area.top + 5 or self.rect.bottom >= self.area.bottom - 5:
                self.movedir = 2 * np.pi - self.movedir
                self.movedir = self.movedir % (2 * np.pi)
                #print("reverse")
                
            newpos = self.rect.move((np.cos(self.movedir)),np.sin(self.movedir))
        self.rect = newpos
        if self.inBlood and pg.time.get_ticks() - self.left_last_footprint > 400:
            self.left_last_footprint = pg.time.get_ticks()
            footprint_dir = round((self.movedir % (2* np.pi)) / (np.pi / 3)) if round((self.movedir % (2* np.pi)) / (np.pi / 3)) < 6 else 5
            self.footprints.append(Footprint(footprint_dir, (self.rect.centerx - 20, self.rect.centery + 35)))
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
    