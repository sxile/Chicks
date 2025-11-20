import os
import pygame as pg

class Button:
    def __init__(self, x, y,image,hover_image, scale, action=None):
        self.img_width = image.get_width()
        self.img_height = image.get_height()
        self.scale = scale
        self.img = image
        self.hover_img = hover_image
        self.image = pg.transform.scale(self.img, (int(self.img_width * scale), int(self.img_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self,surface):
        action = False

        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = pg.transform.scale(self.hover_img, (int(self.img_width * self.scale),int(self.img_height * self.scale)))
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.image = pg.transform.scale(self.img, (int(self.img_width * self.scale), int(self.img_height * self.scale)))
        
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action    
        