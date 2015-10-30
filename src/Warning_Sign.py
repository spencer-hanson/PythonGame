import pygame
import Settings
from Settings import *

class Warning_sign(pygame.sprite.Sprite):
	def __init__(self, posx = -1, posy = -1, rect=None, file="warning.png"):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(file,-1)
		if rect != None:
			self.rect = rect
		self.rect.x = 0
		self.rect.y = Settings.SCREEN_HEIGHT/2-self.rect_height/2
		self.x_vel = 0
		self.y_vel = 0
		self.removeMe = False
		self.wait_ticker = 1800 #Time this message stays on screen.
	
	def update(self):
		if self.wait_ticker > 0:
			self.wait_ticker -= 1
		else:
			self.removeMe = True #Remove self
