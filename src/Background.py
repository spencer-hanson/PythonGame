import pygame
import Settings
from Settings import *

class Background(pygame.sprite.Sprite):
	def __init__(self, posx = -1, posy = -1):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('background.png',-1)
		if posx != -1:
			self.posx = posx
			self.rect.x = posx
		if posy != -1:
			self.posy = posy
			self.rect.y = posy
		
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 10 #Move every 10 frames
		self.posy = posy
		
	def update(self):
		if self.move_ticker == 0:
			self.rect.y += 1
			self.move_ticker = self.MAX_MOVE_TICKER
		elif self.move_ticker > 0:
			self.move_ticker -= 1
		
		if self.rect.y > Settings.SCREEN_HEIGHT:
			self.rect.y = -Settings.BACKGROUND_HEIGHT
