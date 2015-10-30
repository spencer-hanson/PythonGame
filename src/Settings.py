import pygame
from pygame.locals import *

""" CONSTANTS """
global SCREEN_WIDTH 
global SCREEN_HEIGHT 
global BACKGROUND_HEIGHT #Height of background image 
global RESPAWN_TIME

global PLAYER_SPEED

global UP 
global DOWN 
global RIGHT 
global LEFT 

global SHOOT
global ENEMY_BULLET_SPEED

global WAVE1_PASS
global WAVE2_PASS
global WAVE3_PASS

global ENEMY01_HP
global ENEMY02_HP
global ENEMY03_HP
global BOSS_HP

global ENEMY01_BOUNTY
global ENEMY02_BOUNTY
global ENEMY03_BOUNTY


global FONT_SIZE
global SCORE_FORMAT

PLAYER_SPEED = 8/2 

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 480
BACKGROUND_HEIGHT = 420 + 60 #Blazeit
RESPAWN_TIME = 2 #Related to framerate

DOWN = K_DOWN
RIGHT = K_RIGHT
LEFT = K_LEFT
UP = K_UP

ENEMY_BULLET_SPEED = 8
SHOOT = K_z

WAVE1_PASS = 5#5 #Number of enemies needed to kill to advance
WAVE2_PASS = 10#10
WAVE3_PASS = 10#20

ENEMY01_HP = 1
ENEMY02_HP = 1
ENEMY03_HP = 20
BOSS_HP = 300

ENEMY01_BOUNTY = 100
ENEMY02_BOUNTY = 200
ENEMY03_BOUNTY = 500

FONT_SIZE = 28
SCORE_FORMAT = "{0:s} - {1:d}"
#######HELPER FUNCTIONS
def load_image(name, colorkey=None):
	try:
		image = pygame.image.load("images/"+name)
	except pygame.error, message:
		print "Cannot load image:", name
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

def getScreenRect():
	return pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
#######END HELPER FUNCTIONS
