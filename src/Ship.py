import pygame
import Settings
from Settings import *

class Ship_hitbox(pygame.sprite.Sprite):
	def __init__(self, rect):
		pygame.sprite.Sprite.__init__(self)
		xpos = rect.x
		ypos = rect.y

		self.rect = pygame.Rect(xpos+32/2-2, ypos+32/2-2, 4, 4)#player ship size/2 minus half of the size of the hitbox (to center it)
	def updateHitbox(self, rect):
		xpos = rect.x
		ypos = rect.y
		self.rect = pygame.Rect(xpos+32/2-2, ypos+32/2-2, 4, 4)

class Ship(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('ship.png',-1)
		self.rect.x = Settings.SCREEN_WIDTH/2 - self.rect.width/2
		self.rect.y = 5*Settings.SCREEN_HEIGHT/6 #Starting pos
		self.x_dist = Settings.PLAYER_SPEED #How many pixels to move each time
		self.y_dist = Settings.PLAYER_SPEED
		self.invincibility_frames = 0 # Not currently invincible
		self.INVINCIBLE_MAX = 480*2 # frames of invinciblity
		self.hitbox = Ship_hitbox(self.rect)
		self.hitbox_sprite = pygame.sprite.RenderPlain((self.hitbox))
	def resetToStartingPosition(self):
		self.rect.x = Settings.SCREEN_WIDTH/2 - self.rect.width/2
		self.rect.y = 5*Settings.SCREEN_HEIGHT/6
		
	def giveInvinciblity(self):
		self.invincibility_frames = self.INVINCIBLE_MAX
		
	def hasInvincibility(self):
		return (self.invincibility_frames > 0)
	
	def update(self):
		if self.invincibility_frames > 0:
			self.invincibility_frames -= 1

	def move(self):
		keys = pygame.key.get_pressed()
		xMove = 0
		yMove = 0
		if keys[Settings.RIGHT]:
			xMove = self.x_dist
		elif keys[Settings.LEFT]:
			xMove = -self.x_dist
		if keys[Settings.UP]:
			yMove = -self.y_dist
		elif keys[Settings.DOWN]:
			yMove = self.y_dist
		
		if self.rect.x + xMove < 0 or self.rect.x + xMove > Settings.SCREEN_WIDTH - self.rect.width:
			xMove = 0

		
		if self.rect.y + yMove < 0 or self.rect.y + yMove > Settings.SCREEN_HEIGHT - self.rect.height:
			yMove = 0
		
		self.rect.move_ip(xMove, yMove)	
		self.hitbox.updateHitbox(self.rect)

class LivesGroup(object):
	def __init__(self, initalLifeCount):
		self.image, self.rect = load_image('ship.png',-1)
		self.size = self.image.get_size()
		scale_factor = .75
		self.image = pygame.transform.scale(self.image, (int(self.size[0]*scale_factor), int(self.size[1]*scale_factor)))
		self.numLives = initalLifeCount
	def addShip(self):
		self.numLives += 1
	def loseLife(self):
		self.numLives -= 1
	def drawLives(self, screen):
		for i in range(0, self.numLives):
			 screen.blit(self.image, [int(self.size[0] * i), Settings.SCREEN_HEIGHT - self.size[1]])
	def gainLife(self):
		self.addShip()
