import pygame
from GIFImage import *
from Settings import *

class Explosion(pygame.sprite.Sprite):
	def __init__(self, posx = -1, posy = -1):
		pygame.sprite.Sprite.__init__(self)
		file = "images/explosion.gif"
		self.animated_image = GIFImage(file)
		self.rect = pygame.Rect(posx, posy, 16, 16)
		self.removeMe = False
		self.animation_ticker = 0
		self.MAX_TICKER = 240 #Frames of explosion
		if posx != -1:
			self.posx = posx
			self.rect.x = posx
		if posy != -1:
			self.posy = posy
			self.rect.y = posy
	def update(self):
		if self.animation_ticker == 1:
			self.removeMe = True
		if self.animation_ticker == 0:
			self.animation_ticker = self.MAX_TICKER
		elif self.animation_ticker > 0:
			self.animation_ticker -= 1
			
