import pygame as pg

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale):
		image = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pg.transform.scale(image, (width * scale, height * scale))

		return image