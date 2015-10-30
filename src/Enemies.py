import pygame
import random
import math
import Settings
from Settings import *
from Bullets import *

class Enemy(pygame.sprite.Sprite):
	def __init__(self, posx = -1, posy = -1, rect=None, file="DONT_CREATE_ME"):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(file,-1)
		if rect != None:
			self.rect = rect
		self.rect.x = Settings.SCREEN_WIDTH/2-self.rect.width/2
		self.rect.y = Settings.SCREEN_HEIGHT/4
		self.x_vel = 0
		self.y_vel = 0
		self.removeMe = False
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 0
		self.bullet_queue = []
		if posx != -1:
			self.posx = posx
			self.rect.x = posx
		if posy != -1:
			self.posy = posy
			self.rect.y = posy
		self.playerx = 0
		self.playery = 0
		self.hp = 1 #1 hit ko
		self.bounty = 100 #Initial enemy bounty is 100 points	
	
	def setPlayerPos(self, playerx, playery):
		self.playerx = playerx
		self.playery = playery

	def getBulletVectors(self):
		xdist = self.playerx - self.rect.x
		ydist = self.playery - self.rect.y
		zdist = math.sqrt(math.pow(xdist, 2) + math.pow(ydist, 2))
		bul_x_vel = xdist/zdist * Settings.ENEMY_BULLET_SPEED
		bul_y_vel = ydist/zdist * Settings.ENEMY_BULLET_SPEED
		return (bul_x_vel, bul_y_vel)
	
			
class Enemy01(Enemy): #Enemy type 1 "Rammer"
	def __init__(self, posx = -1, posy = -1, rect=None, file="enemy_01.png"):
		Enemy.__init__(self, posx, posy, rect, file)
		#self.image, self.rect = load_image(file,-1)
		self.rect.x = random.randint(0, Settings.SCREEN_WIDTH-self.rect.width) #Spawns in a random position above the screen
		self.rect.y = -32
		self.x_vel = 0
		self.y_vel = 5
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 20
		self.hp = Settings.ENEMY01_HP
		self.bounty = Settings.ENEMY01_BOUNTY
	
	def update(self):
		if self.move_ticker == 0:
			self.rect.move_ip(self.x_vel, self.y_vel)
			self.move_ticker = self.MAX_MOVE_TICKER
		else:
			self.move_ticker -= 1
		
		if self.rect.y > Settings.SCREEN_HEIGHT: #delete if it flies off bottom edge.
			removeMe = True

class Enemy02(Enemy): #Enemy type 2 "Shooter"
	def __init__(self, posx = -1, posy = -1, rect=None, file="enemy_02.png"):
		Enemy.__init__(self, posx, posy, rect, file)
		self.hp = Settings.ENEMY02_HP
		self.rect.x = random.randint(0, Settings.SCREEN_WIDTH-self.rect.width) #Spawns in a random position above the screen
		self.rect.y = -32
		self.x_vel = 0
		self.y_vel = 3
		self.exit_vel = -self.y_vel
		self.leaving = False #this variable checks if it's already fired off a shot and is now leaving.
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 20
		self.wait_ticker = 300 #Delay before shooting.
		self.bounty = Settings.ENEMY02_BOUNTY
		
	def update(self):
		x = self.rect.x
		y = self.rect.y
		
		if y < Settings.SCREEN_HEIGHT/4 and self.leaving == False: #y coordinate where the enemy should roughly stop moving
			if self.move_ticker == 0:
				self.rect.move_ip(self.x_vel, self.y_vel)
				self.move_ticker = self.MAX_MOVE_TICKER
			else:
				self.move_ticker -= 1
		elif y >= Settings.SCREEN_HEIGHT/4 and self.leaving == False:
			if self.wait_ticker > 0: #delay before shooting.
				self.wait_ticker -= 1
			else:
				tmp = random.randint(0,4)
				if tmp == 0 or tmp == 1 or tmp == 2: #3/4 of the time shoot tracking shots
					tmp_bullet = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))#Bullet is 16x16 px
					tmp_bullet.rect.x = self.rect.x + self.rect.width/2 - 16/2
					tmp_bullet.rect.y = self.rect.y + self.rect.height
					
					vects = self.getBulletVectors()
					
					tmp_bullet.x_vel = vects[0]
					tmp_bullet.y_vel = vects[1]
					
					self.bullet_queue.append(tmp_bullet)
				else: #Shoot a straight shot
					tmp_bullet = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))
					tmp_bullet.x_vel = 0
					tmp_bullet.y_vel = 6
					tmp_bullet.rect.x = self.rect.x + self.rect.width/2 - 16/2
					tmp_bullet.rect.y = self.rect.y + self.rect.height
					self.bullet_queue.append(tmp_bullet)
				self.leaving = True
		else: #leave
			if self.move_ticker == 0:
				self.rect.move_ip(self.x_vel, self.exit_vel)
				self.move_ticker = self.MAX_MOVE_TICKER
			else:
				self.move_ticker -= 1
		if self.rect.y < 0 and self.leaving == True: #delete after flying offscreen after shooting.
			removeMe = True
			
class Enemy03(Enemy): #Enemy type 3 "Brute"
	def __init__(self, posx = -1, posy = -1, rect=None, file="enemy_03.png"):
		Enemy.__init__(self, posx, posy, rect, file)
		self.hp = Settings.ENEMY03_HP #hits to kill
		if random.randint(0,1) == 0:
			self.rect.x = -32 #Default x
			self.x_vel = 3
			self.xbound = Settings.SCREEN_WIDTH #Check which boundary to remove enemy.
		else:
			self.rect.x = Settings.SCREEN_WIDTH + 32
			self.x_vel = -3
			self.xbound = 0
		
		self.rect.y = 32
		x = self.rect.x
		y = self.rect.y
		self.y_vel = 1
		
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 20
		self.wait_ticker = 300 #Delay before shooting.
		self.MAX_WAIT_TICKER = 300
		self.shoot_ticker = 0
		self.MAX_SHOOT_TICKER = 70 #time between shots
		self.shooting = False
		self.shot_counter = 0
		self.bounty = Settings.ENEMY03_BOUNTY
	
	def update(self):
		x = self.rect.x
		y = self.rect.y
		
		if self.move_ticker == 0:
			self.rect.move_ip(self.x_vel, self.y_vel)
			self.move_ticker = self.MAX_MOVE_TICKER
		else:
			self.move_ticker -= 1
		
		if self.wait_ticker == 0: #Start Shooting
			self.shooting = True
		else:
			self.wait_ticker -=1
		
		if self.shooting:
			if self.shot_counter < 5:
				if self.shoot_ticker == 0:
					self.shot_counter += 1
					tmp_bullet = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))#16x16 is size of bullet png
					tmp_bullet.x_vel = 0
					tmp_bullet.y_vel = 6
					tmp_bullet.rect.x = self.rect.x + self.rect.width/2 - 16/2
					tmp_bullet.rect.y = self.rect.y + self.rect.height
					self.bullet_queue.append(tmp_bullet)
					self.shoot_ticker = self.MAX_SHOOT_TICKER
				else:
					self.shoot_ticker -= 1
			else:
				self.shooting = False
				self.shot_counter = 0
				self.wait_ticker = self.MAX_WAIT_TICKER #stop shooting and prepare for next volley.
			
		if self.xbound != 0:
			if self.rect.x > self.xbound: #delete after flying offscreen opposite to starting side.
				removeMe = True
		else:
			if self.rect.x < self.xbound:
				removeMe = True

class Boss(Enemy): #Boss
	def __init__(self, posx = -1, posy = -1, rect=None, file="boss.png"):
		Enemy.__init__(self, posx, posy, rect, file)
		self.image, self.rect = load_image(file,-1)
		self.rect.x = Settings.SCREEN_WIDTH/2 - self.rect.width/2
		self.rect.y = -64
		self.x_vel = 3
		self.y_vel = 5
		self.shot_counter = 0
		self.move_ticker = 0
		self.MAX_MOVE_TICKER = 20
		self.loop_ticker = 6000 #Initial attack pattern + initial delay
		self.MAX_LOOP_TICKER = 5400 #Attack pattern length
		self.shoot_ticker = 0
		self.MAX_SHOOT_TICKER = 180 #time between shots
		self.PATTERN_4_MAX_TICKER = 60 #time between shots in pattern 4
		self.hp = Settings.BOSS_HP
		self.bounty = 10000
		self.stopped = False
		self.reverse_dir = True
	
	def update(self):
		x = self.rect.x
		y = self.rect.y
		if y < Settings.SCREEN_HEIGHT/6: #Move onto first 1/6 of screen
			if self.move_ticker == 0:
				self.rect.move_ip(0, self.y_vel)
				self.move_ticker = self.MAX_MOVE_TICKER
			else:
				self.move_ticker -= 1
		else:
			if self.move_ticker == 0:
				self.rect.move_ip(self.x_vel, 0)
				self.move_ticker = self.MAX_MOVE_TICKER
			else:
				self.move_ticker -= 1
		
		if self.reverse_dir == False:
			self.x_vel = 0	
		else:
			if self.rect.x < 0 or self.rect.x > Settings.SCREEN_WIDTH - self.rect.width: #Move back and forth
				self.x_vel = -self.x_vel
			
		if self.loop_ticker == 0: #Start Shooting
			self.loop_ticker = self.MAX_LOOP_TICKER
		else:
			self.loop_ticker -=1
		
		if self.loop_ticker < 5400 and self.loop_ticker > 4800:
			if self.reverse_dir == False:
				if random.randint(0,1) == 0:
					self.x_vel = 3
				else:
					self.x_vel = -3
				self.reverse_dir = True
			if self.shoot_ticker == 0:
				#Bullet code here pls Zach :) (And the other patterns too)
				tmp_bullet = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))
				tmp_bullet.x_vel = 0
				tmp_bullet.y_vel = 6
				tmp_bullet.rect.x = self.rect.x + self.rect.width/2 - 16/2
				tmp_bullet.rect.y = self.rect.y + self.rect.height
				self.bullet_queue.append(tmp_bullet)
				
				self.shoot_ticker = self.MAX_SHOOT_TICKER
			else:
				self.shoot_ticker -= 1
		elif self.loop_ticker < 4200 and self.loop_ticker > 3000:
			if self.shoot_ticker == 0:
				#self.shot_counter += 1
					#Bullet creation code for pattern number 2 goes here
				tmp_bullet1 = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))#Bullet is 16x16 px
				tmp_bullet1.rect.x = self.rect.x + 8
				tmp_bullet1.rect.y = self.rect.y + 8
				tmp_bullet2 = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))#Bullet is 16x16 px
				tmp_bullet2.rect.x = self.rect.x + self.rect.width-8
				tmp_bullet2.rect.y = self.rect.y + 8
					
				vects = self.getBulletVectors()
					
				tmp_bullet1.x_vel = vects[0]
				tmp_bullet1.y_vel = vects[1]
				
				vects2 = self.getBulletVectors()
				
				tmp_bullet2.x_vel = vects2[0]
				tmp_bullet2.y_vel = vects2[1]
					
				self.bullet_queue.append(tmp_bullet1)
				self.bullet_queue.append(tmp_bullet2)
				
				self.shoot_ticker = self.MAX_SHOOT_TICKER
			else:
				self.shoot_ticker -= 1
		elif self.loop_ticker < 2400 and self.loop_ticker > 1800:
			if self.shoot_ticker == 0:
				#self.shot_counter += 1
					#Bullet creation code for pattern number 3 goes here
				tmp_bullet = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))
				tmp_bullet.x_vel = 0
				tmp_bullet.y_vel = 9
				tmp_bullet.rect.x = self.rect.x + self.rect.width/2 - 16/2
				tmp_bullet.rect.y = self.rect.y + self.rect.height
				self.bullet_queue.append(tmp_bullet)
				
				tmp_bullet1 = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))#Bullet is 16x16 px
				tmp_bullet1.rect.x = self.rect.x + 8
				tmp_bullet1.rect.y = self.rect.y + 8
				tmp_bullet2 = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))#Bullet is 16x16 px
				tmp_bullet2.rect.x = self.rect.x + self.rect.width-8
				tmp_bullet2.rect.y = self.rect.y + 8
					
				vects = self.getBulletVectors()
					
				tmp_bullet1.x_vel = vects[0]
				tmp_bullet1.y_vel = vects[1]
				
				vects2 = self.getBulletVectors()
				
				tmp_bullet2.x_vel = vects2[0]
				tmp_bullet2.y_vel = vects2[1]
					
				self.bullet_queue.append(tmp_bullet1)
				self.bullet_queue.append(tmp_bullet2)
				self.shoot_ticker = self.MAX_SHOOT_TICKER
			else:
				self.shoot_ticker -= 1
		elif self.loop_ticker < 1200 and self.loop_ticker > 600:
			self.reverse_dir = False
			if self.shoot_ticker == 0:
				#Bullet creation code for pattern number 4 goes here
					if self.shot_counter <= 7:
						if self.shot_counter == 0:
							tmp_bullet = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))
							tmp_bullet.x_vel = 0
							tmp_bullet.y_vel = 7
							tmp_bullet.rect.x = self.rect.x + self.rect.width/2 - 16/2
							tmp_bullet.rect.y = self.rect.y + self.rect.height
							self.bullet_queue.append(tmp_bullet)
						else:
							tmp_bullet1 = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))
							tmp_bullet1.x_vel = 0
							tmp_bullet1.y_vel = 7
							tmp_bullet1.rect.x = (self.rect.x + self.rect.width/2 - 16/2) + (8 * self.shot_counter)
							tmp_bullet1.rect.y = self.rect.y + self.rect.height
							
							tmp_bullet2 = EBullet(pygame.Rect(self.rect.x + (self.rect.width/2), self.rect.y + self.rect.height, 16, 16))
							tmp_bullet2.x_vel = 0
							tmp_bullet2.y_vel = 7
							tmp_bullet2.rect.x = (self.rect.x + self.rect.width/2 - 16/2) - (8 * self.shot_counter)
							tmp_bullet2.rect.y = self.rect.y + self.rect.height
							
							self.bullet_queue.append(tmp_bullet1)
							self.bullet_queue.append(tmp_bullet2)
						self.shot_counter += 1
					else:
						self.shot_counter = 0
					self.shoot_ticker = self.PATTERN_4_MAX_TICKER
			else:
				self.shoot_ticker -= 1

class BossWarning(pygame.sprite.Sprite):
	def __init__(self, posx = -1, posy = -1, rect=None, file="warning.png"):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(file,-1)
		if rect != None:
			self.rect = rect
		self.rect.x = 0
		self.rect.y = Settings.SCREEN_HEIGHT/2-self.rect.height/2
		self.removeMe = False
		self.stay_ticker = 1200
	
	def update(self):
		if self.stay_ticker > 0:
			self.stay_ticker -= 1
		if self.stay_ticker == 0:
			removeMe = True
			#Put some code letting the game know to spawn the boss or something here.
