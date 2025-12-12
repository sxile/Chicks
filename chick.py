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
        sleeping_spritesheet_image = pg.image.load('data/chick_sleeping.png').convert_alpha()
        death_spritesheet_image = pg.image.load('data/chick_death.png').convert_alpha()
        
        standing_spritesheet = SpriteSheet(standing_spritesheet_image)
        walking_spritesheet = SpriteSheet(walking_spritesheet_image)
        sleeping_spritesheet = SpriteSheet(sleeping_spritesheet_image)
        death_spritesheet = SpriteSheet(death_spritesheet_image)

        self.standing_frames = [None,None]
        self.walking_frames = [None,None,None,None,None,None]
        self.sleeping_frames = [None, None, None, None]
        self.death_frames = [None,None,None,None,None,None,
                        None,None,None,None,None,None,
                        None,None,None,None,None,None,
                        None]


        self.standing_frames = [standing_spritesheet.get_image(0, 25, 28, 4),standing_spritesheet.get_image(1, 25, 28, 4)]
        for i in range(6):
            self.walking_frames[i] = walking_spritesheet.get_image(i, 25, 28, 4)
        for i in range(4):
            self.sleeping_frames[i] = sleeping_spritesheet.get_image(i, 25, 28, 4)

        for i in range(19):
            self.death_frames[i] = death_spritesheet.get_image(i, 25, 28, 4)


        # Initialization
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.dead = False
        self.nap_time = True
        self.awake = True
        self.pos = ((np.random.rand() * 400) + 200, (np.random.rand() * 300) + 100)
        self.screen = pg.display.get_surface()
        self.area = self.screen.get_rect()
        self.rect.topleft = self.pos

        self.hitbox = pg.Rect(self.rect.left, self.rect.top + 70, 100, 42)

        self.movedir = 7
        self.inBlood = False
        self.footprints = []
        self.left_last_footprint = pg.time.get_ticks()
        self.walked_through_blood = 0
        self.facing_left = False
        #print(self.movedir)

    # Update Sprite
    def update(self, screen):
        # Print footprints, if any
        for fprint in self.footprints:
            fprint.draw(screen)
        # If chick still alive
        if not self.dead:
            # If not sleeping
            if self.awake:
                # If left blood pool 10 seconds ago, stop leaving trail
                if pg.time.get_ticks() - self.walked_through_blood > 10000:
                    self.inBlood = False
                # Change Direction
                if np.random.rand() < 0.01:
                    # if > 2pi, dont move. if 0 < movedir < 2pi move.
                    self.movedir = np.random.rand() * (2 * np.pi + 5) 
                    self.animation_timer = pg.time.get_ticks() + (np.random.rand() * 1000)
                # Decide to walk, or stand/sleep
                if self.movedir < (2 * np.pi):
                    self.move()
                else:
                    # Maybe go to sleep
                    if self.nap_time and self.movedir > (2 * np.pi + 5) - 0.15:
                        self.awake = False
                        self.started_sleeping = pg.time.get_ticks()
                        self.sleeping_timer = (np.random.rand() * 5) + 10
                    # Otherwise, stand and blink
                    if (self.animation_timer - pg.time.get_ticks()) % 1000 > 890:
                        self.image = self.standing_frames[1]
                    else:
                        self.image = self.standing_frames[0]
                    if self.facing_left:
                        self.image = pg.transform.flip(self.image, True, False)
            # If sleeping
            else:
                # Wake up or animate sleep
                if (pg.time.get_ticks() - self.started_sleeping) / 1000 > self.sleeping_timer:
                    self.awake = True
                    self.movedir = self.movedir - 0.5
                frame = 0 if ((pg.time.get_ticks() - self.animation_timer) % 1000) > 500 else 1
                if self.facing_left:
                        frame = frame + 2
                self.image = self.sleeping_frames[frame]
        # If chick is dead/dying
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
            if self.facing_left:
                self.image = pg.transform.flip(self.image,True, False)
    
    # Walk
    def move(self):
        # Move in direction movedir
        # 0 < movedir < 2pi, used as radian 
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
        # Update position & hitboxes
        self.rect = newpos
        self.hitbox = pg.rect.Rect(newpos.x + 30, newpos.y + 95, 40, 10)
        if self.inBlood and pg.time.get_ticks() - self.left_last_footprint > 400:
            self.left_last_footprint = pg.time.get_ticks()
            footprint_dir = round((self.movedir % (2* np.pi)) / (np.pi / 3)) if round((self.movedir % (2* np.pi)) / (np.pi / 3)) < 6 else 0
            self.footprints.append(Footprint(footprint_dir, (self.rect.centerx - 20, self.rect.centery + 35)))
        self.image = self.walking_frames[int(((self.animation_timer - pg.time.get_ticks()) % 1000) / 167)]
        if self.movedir > np.pi / 2 and self.movedir < np.pi * 1.5:
            self.image = pg.transform.flip(self.image, True, False)
            self.facing_left = True
        else:
            self.facing_left = False

    # Wake up chicks and prevent them from sleeping
    def wake_up(self):
        self.nap_time = False
        self.awake = True
        self.movedir = self.movedir - 0.5

    # Allow chicks to sleep again
    def start_nap_time(self):
        self.nap_time = True

    # If chick walks through a dead chick, track bloody footprints
    def standingInBlood(self):
        if not self.dead:
            # if not self.inBlood:
            #     print("stepped in blood")
            self.inBlood = True
            self.walked_through_blood = pg.time.get_ticks()

    # Kill the chick
    def kill(self):
        if self.dead:
            return False
        else:
            self.image = self.standing_frames[0]
            self.animation_timer = pg.time.get_ticks() + 2000
            self.dead = True
            self.hitbox = pg.rect.Rect(self.rect.left, self.rect.bottom - 24, 100, 24)
            return True
    
    