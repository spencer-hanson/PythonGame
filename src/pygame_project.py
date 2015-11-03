import os, sys
import random
import pygame
import Settings

import GIFImage
import inputbox


from pygame.locals import *
from Enemies import *
from Explosion import *
from Background import *
from Ship import *
from Bullets import *
from Music import *
from EightCrypt import *

if not pygame.font: print "Warning, fonts disabled!"
if not pygame.mixer: print "Warning, sound disabled!"



class Main:
	def __init__(self, width=Settings.SCREEN_WIDTH,height=Settings.SCREEN_HEIGHT):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.shooting = False
		self.shoot_ticker = 0 #Can shoot without waiting
		self.MAX_SHOOT_TICKER = 30 #One shot every x frames
		self.spawn_ticker = 1800 #Start spawning 1800 frames in.
		self.MAX_SPAWN_TICKER = 1800 #Max one new enemy every 1800 frames
		self.GAME_OVER = False
		self.END_GAME = False
		self.END_CREDITS = False
		self.RESPAWNING = False
		self.respawn_ticker = 0
		
		self.SCORE = 0##################
		self.HIGHSCORES = []
		self.checkHighscore()
		
		self.wave1_pass = False
		self.wave2_pass = False
		self.wave3_pass = False
		self.boss_spawned = False
		self.enemies_killed = 0 #Number of enemy01 killed
		
		self.music = Music("MainLoop")
		
		self.clock = pygame.time.Clock()
		self.LIVES = 3#############
		
	def getScores(self):
		scores = {}
		count = 0
		for line in self.HIGHSCORES:
			data = line.split("-")
			name = str(data[0].strip())
			data[1] = data[1].strip().strip('\0')
			score = int(data[1])
			scores[Settings.SCORE_FORMAT.format(line, count)] = score
			count += 1
		return scores

	def getRank(self, key, value, scores):
		rank = 0
		for key2, value2 in scores.iteritems():
			if key != key2:
				if value < value2:
					rank += 1	
		return rank	
			
	def getEntries(self, scores):
		entries = []
		ranks = []
		#KNOWN BUG##
		"""
		If there are more than two scores that are next to eachother
		the bump algorithm will move the new value to the next one, but that will also be taken
		A fix to this is to loop through again to make sure the newly bumped value doesn't already
		exist, but then you would need n loops, where n is the number of numbers close to eachother
		To replicate, create a large array of self.HIGHSCORES using random numbers, and it's bound to happen at least once
		"""
		for key, value in scores.iteritems():
			new_rank = self.getRank(key, value, scores)
			#print key,value,new_rank#####################
			bump = False
			
			#Doot doot gross code here
			for rank in ranks:
				if new_rank == rank:#Find index for bumpin
					bump = True
				if bump == True:
					new_rank += 1
			############			
			ranks.append(new_rank)
		
		count2 = 0
		for key, value in scores.iteritems():
			entries.append([str(key.split("-")[0].strip()), value, ranks[count2]])  #["nobody", 0, 3] name,score,rank
			count2 += 1
		return entries

	def sortEntries(self, entries):
		new_entries = []
		#print entries########################
		for i in range(len(entries)):
			new_entries.append(i)
		
		for entry in entries:
			####3print entry[0],entry[1],entry[2]
			new_entries[entry[2]] = Settings.SCORE_FORMAT.format(entry[0], entry[1])
		return new_entries	

	def setHighscore(self, name):
		eightcrypt = EightCrypt()
		
		new_entry = Settings.SCORE_FORMAT.format(name, self.SCORE)
		self.HIGHSCORES = self.sortEntries(self.getEntries(self.getScores()))
		self.HIGHSCORES.append(new_entry)
		self.HIGHSCORES = self.sortEntries(self.getEntries(self.getScores()))
		
		#print self.HIGHSCORES##############
		eightcrypt.write("highscores.txt", self.HIGHSCORES)
		
	def checkHighscore(self):
		eightcrypt = EightCrypt()
		if os.path.isfile("highscores.txt") == False:
			eightcrypt = EightCrypt()
			self.HIGHSCORES.append("Chuck Norris - 999999")
			self.HIGHSCORES.append("player 1 - 1001001")
			self.HIGHSCORES.append("bush - 2001")
			self.HIGHSCORES.append("John Cena - 10")
			self.HIGHSCORES.append("Liz Boese - 1")
			eightcrypt.write("highscores.txt", self.HIGHSCORES)
		else:
			eightcrypt = EightCrypt()
			self.HIGHSCORES = eightcrypt.read("highscores.txt")
			
			
	def explosivifySprite(self, sprite_rect, explosionCount=4): #Explode around a sprite, optional explosions count
		for i in range(0,explosionCount):
			x_pos = sprite_rect.x - int(.4 * sprite_rect.width)
			y_pos = sprite_rect.y - int(.4 * sprite_rect.height)
			offset_x = random.randint(0,sprite_rect.width + int(.4 * sprite_rect.width))
			offset_y = random.randint(0,sprite_rect.height + int(.4 * sprite_rect.height)) #40% increased explosion radius >:)
			self.explosion_sprites.add(Explosion(x_pos + offset_x, y_pos + offset_y))

	def LoadSprites(self):
		self.ship = Ship()
		self.ship_sprite = pygame.sprite.RenderPlain((self.ship))
		self.bullet_sprites = pygame.sprite.Group() #Make a group of bullets
		self.en_bullet_sprites = pygame.sprite.Group() 
		self.enemy_sprites = pygame.sprite.Group() #Groups enemies
		self.backgrounds = pygame.sprite.Group()
		self.explosion_sprites = pygame.sprite.Group()
		self.ship_lives_sprites = LivesGroup(self.LIVES)
		self.last_death_rect = self.ship.rect
		self.font = pygame.font.Font(None, Settings.FONT_SIZE) #No specific font, size
		
	def updateSprites(self):
		self.ship.update()
		self.bullet_sprites.update()
		self.en_bullet_sprites.update()
		self.backgrounds.update()
		self.enemy_sprites.update()
		for enemy in self.enemy_sprites: #Update player pos for all enemies
			enemy.setPlayerPos(self.ship.rect.x, self.ship.rect.y)
			if len(enemy.bullet_queue) > 0: #Move bullets from enemy bullet queue to render group
				for en_bullet in enemy.bullet_queue:
					self.en_bullet_sprites.add(en_bullet)
					enemy.bullet_queue.remove(en_bullet)
		self.explosion_sprites.update()
		
	def checkShoot(self):
		if self.shoot_ticker > 0:
				self.shoot_ticker -= 1
		if self.shooting and self.shoot_ticker == 0:
				tmp_bullet = Bullet(pygame.Rect(self.ship.rect.x + (self.ship.rect.width/2), self.ship.rect.y, 16, 4))
				tmp_bullet.rect.x = tmp_bullet.rect.x - tmp_bullet.rect.height/2 #center (.height cuz flipped)
				tmp_bullet.image = pygame.transform.rotate(tmp_bullet.image, 90)
				self.bullet_sprites.add(tmp_bullet)
				self.shoot_ticker = self.MAX_SHOOT_TICKER
				

	def spawnEnemies(self):
		#Wave 1
		if self.enemies_killed < Settings.WAVE1_PASS and self.wave1_pass == False:
			if self.spawn_ticker > 0:
				self.spawn_ticker -= 1
			elif self.spawn_ticker == 0:
				new_enemy = Enemy01()
				self.enemy_sprites.add(new_enemy)
				self.spawn_ticker = self.MAX_SPAWN_TICKER
		elif self.enemies_killed >= Settings.WAVE1_PASS and self.wave1_pass == False:
			self.enemies_killed = 0
			self.wave1_pass = True
		#Wave 2
		if self.enemies_killed < Settings.WAVE2_PASS and self.wave2_pass == False and self.wave1_pass == True:
			if self.spawn_ticker > 0:
				self.spawn_ticker -= 1
			elif self.spawn_ticker == 0:
				tmp = random.randint(0,1)
				if tmp == 0:
					new_enemy1 = Enemy01()
					self.enemy_sprites.add(new_enemy1)
				new_enemy = Enemy02()
				self.enemy_sprites.add(new_enemy)
				self.spawn_ticker = self.MAX_SPAWN_TICKER
		elif self.enemies_killed >= Settings.WAVE2_PASS and self.wave2_pass == False:
			self.enemies_killed = 0
			self.wave2_pass = True
		#Wave 3
		if self.enemies_killed < Settings.WAVE3_PASS and self.wave3_pass == False and self.wave1_pass == True and self.wave2_pass == True:
			if self.spawn_ticker > 0:
				self.spawn_ticker -= 1
			elif self.spawn_ticker == 0:
				tmp = random.randint(0,2)
				if tmp == 0:
					new_enemy1 = Enemy01()
					self.enemy_sprites.add(new_enemy1)
				tmp = random.randint(0,3)
				if tmp == 0:
					new_enemy2 = Enemy02()
					self.enemy_sprites.add(new_enemy2)
				new_enemy = Enemy03()
				self.enemy_sprites.add(new_enemy)
				self.spawn_ticker = self.MAX_SPAWN_TICKER
		elif self.enemies_killed >= Settings.WAVE3_PASS and self.wave3_pass == False:
			self.enemies_killed = 0
			self.wave3_pass = True
		#Boss
		if self.wave1_pass and self.wave2_pass and self.wave3_pass and self.boss_spawned == False:
			self.enemy_sprites.add(Boss())
			self.music = Music("Blaze")
			self.music.play()
			self.boss_spawned = True

	def checkCollisions(self):
		hit_enemies = pygame.sprite.groupcollide(self.enemy_sprites, self.bullet_sprites, False, True) #Check collide between two sprite groups, remove bullet on true collision
		for enemy in hit_enemies:
			if enemy.hp - 1 <= 0:
				self.explosivifySprite(enemy.rect)
				self.SCORE += enemy.bounty
				self.enemies_killed += 1
				enemy.removeMe = True
			else:
				enemy.hp -= 1
				self.explosivifySprite(enemy.rect, 1)

		if self.ship.hasInvincibility() == False:
			player_isHit = False
			hit_sprites = pygame.sprite.groupcollide(self.enemy_sprites, self.ship.hitbox_sprite, False, False) #Check between ship and enemies
			for enemy_sprite in hit_sprites:
				player_isHit = True
				self.explosivifySprite(enemy_sprite.rect)
				enemy_sprite.removeMe = True
				self.enemies_killed += 1
				
			hit_sprites = pygame.sprite.groupcollide(self.en_bullet_sprites, self.ship.hitbox_sprite, False, False)
			for enemy_bullet in hit_sprites: 
				player_isHit = True
				enemy_bullet.removeMe = True
						
			if player_isHit == True:
				self.LIVES -= 1
				self.last_death_rect = self.ship.rect
				self.ship_lives_sprites.loseLife()
				self.respawn_ticker = Settings.RESPAWN_TIME * 120 * 2 # fps x seconds x 2(for explosion and respawn) = frames to respawn
				self.RESPAWNING = True

		if self.LIVES < 1: #Classic game programming 'if' statement :)
			self.GAME_OVER = True

	def handleEvents(self):
		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT:
					sys.exit()
			elif event.type == KEYDOWN: #Key presses
				self.ship.move() #Move the ship
				if keys[Settings.SHOOT]:
					self.shooting = True
			elif event.type == KEYUP: 
				if keys[Settings.SHOOT] != True:
					self.shooting = False

	def drawSprites(self):
		self.screen.blit(self.clear_bg, (0,0))
		self.backgrounds.draw(self.screen)
		if self.ship.hasInvincibility():
			if self.ship.invincibility_frames % 3 == 0: #Only draw every x frames, respawn "flickering"
					self.ship_sprite.draw(self.screen)
			
		else:
			self.ship_sprite.draw(self.screen)
		
		self.bullet_sprites.draw(self.screen)
		self.en_bullet_sprites.draw(self.screen)
		self.enemy_sprites.draw(self.screen)
		
		for explosion in self.explosion_sprites:
			explosion.animated_image.render(self.screen, (explosion.rect.x, explosion.rect.y))
		
		self.ship_lives_sprites.drawLives(self.screen)

	def cleanupSprites(self):
		for bullet1 in self.bullet_sprites: #Dem bullets
			if bullet1.removeMe == True:
				self.bullet_sprites.remove(bullet1)
		for explosion in self.explosion_sprites: #Explosionssss
			if explosion.removeMe == True:
				self.explosion_sprites.remove(explosion)
				
		for enemy in self.enemy_sprites: #Enemies
			if enemy.removeMe == True:
				self.enemy_sprites.remove(enemy)	

		for bullet2 in self.en_bullet_sprites: #Enemy bullets
			if bullet2.removeMe == True:
				self.en_bullet_sprites.remove(bullet2)
	
	def gameOver(self): #GG!
		self.END_GAME = True
		pygame.key.set_repeat(120, 60)
		name = inputbox.ask(self.screen, "GG! Your name?")
		self.setHighscore(name)
		
	def drawScore(self):
		text = self.font.render("{0:d}".format(self.SCORE), 1, (255, 255, 0))
		textpos = text.get_rect()
		textpos.x = Settings.SCREEN_WIDTH/2
		textpos.y = Settings.SCREEN_HEIGHT - Settings.FONT_SIZE
		self.screen.blit(text, textpos)

	def MainLoop(self):
		self.LoadSprites()
		pygame.key.set_repeat(10, 20)#Input every 20ms, read every 10mss
		
		#Clear background
		self.backgrounds.add(pygame.sprite.RenderPlain(Background(0,0*Settings.BACKGROUND_HEIGHT)))
		self.backgrounds.add(pygame.sprite.RenderPlain(Background(0,1*Settings.BACKGROUND_HEIGHT)))
		self.backgrounds.add(pygame.sprite.RenderPlain(Background(0,2*Settings.BACKGROUND_HEIGHT)))
		
		self.clear_bg = pygame.Surface(self.screen.get_size())
		self.clear_bg = self.clear_bg.convert()
		self.clear_bg.fill((0,0,0))
		
		self.music.play()
		
		while self.END_GAME != True:
			self.clock.tick(600) #Cap framerate at 60 fps
			if self.RESPAWNING == True:
				if self.respawn_ticker % 120 == 0 and self.respawn_ticker > 119: #Periodic explosions, leaving 120 frames for respawn "stillness", but still exploding at frame = 120
					self.explosivifySprite(self.last_death_rect)
				elif self.respawn_ticker < 120:
					self.ship.resetToStartingPosition()
				if self.respawn_ticker == 0:
					if self.GAME_OVER:
						self.gameOver()
					else:
						self.ship.giveInvinciblity()
						self.RESPAWNING = False
				self.respawn_ticker -= 1
			else:
				#Event checking
				self.handleEvents()
				#Check if player can shoot
				self.checkShoot()
				#Collisions
				self.checkCollisions()
			####End RESPAWNING if statement - WARNING!! - anything outside will run during respawn!
			
			#Update sprites
			self.updateSprites()
			#Spawn enemies
			self.spawnEnemies()
			#Drawing sprites
			self.drawSprites()
			#Update score
			self.drawScore()
			
			pygame.display.flip()
			
			#Clean all entity groups up	
			self.cleanupSprites()
			#########
			credits_ticker = 600 * len(self.HIGHSCORES) * 2
		while self.END_CREDITS != True:
			font = pygame.font.Font(None, 36) #No specific font, size 36 pt
			text = font.render("GAME OVER!", 1, (255, 0, 0))#Gameover in red -> (255,0,0)
			textpos = text.get_rect()
			textpos.centerx = Settings.SCREEN_WIDTH/2
			
			

			credits_ticker -= 1
			if credits_ticker <= 0:
				self.END_CREDITS = True
			self.drawSprites()
			
			for i in range(len(self.HIGHSCORES)):
				scores = self.font.render(self.HIGHSCORES[i], 1, (255, 255, 0))
				textpos2 = scores.get_rect()
				textpos2.centerx = Settings.SCREEN_WIDTH/2
				textpos2.y = (i+2)*Settings.FONT_SIZE
				self.screen.blit(scores, textpos2)
			self.screen.blit(text, textpos)
			
			self.explosion_sprites.update()
			self.cleanupSprites() #Remove explosions
			pygame.display.flip()
			
		#Outside game loop
		#annnnddd, quit! (Thanks Mr. Skeletal)

if __name__ == "__main__":
	MainWindow = Main()
	MainWindow.MainLoop()
