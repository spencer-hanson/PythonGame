import pygame
from pygame.locals import *
from pygame_project import *
import Settings
from Settings import *


class Bullet(pygame.sprite.Sprite):
	def __init__(self, rect=None, file="shot.png"):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(file,-1)
		if rect != None:
			self.rect = rect
		self.x_vel = 0
		self.y_vel = -4
		self.removeMe = False
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 2 #move every 10 frames
	def update(self):
		if self.move_ticker == 0:
			self.rect.move_ip(self.x_vel, self.y_vel)
			self.move_ticker = self.MAX_MOVE_TICKER
		else:
			self.move_ticker -= 1
		
		if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
			self.removeMe = True


class EBullet(Bullet): #Enemy bullets
	def __init__(self, posx = -1, posy = -1, rect=None, file="projectile_01.png"):
		Bullet.__init__(self)
		self.image, self.rect = load_image(file,-1)
		if rect != None:
			self.rect = rect
		self.x_vel = 0
		self.y_vel = 0 
		self.removeMe = False
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 20
	def update(self):
		if self.move_ticker == 0:
			self.rect.move_ip(self.x_vel, self.y_vel)
			self.move_ticker = self.MAX_MOVE_TICKER
		else:
			self.move_ticker -= 1
		
		if self.rect.x < 0 or self.rect.x > Settings.SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > Settings.SCREEN_HEIGHT:
			self.removeMe = True
