import pygame
import Settings
from Settings import *

class Music(object):
	def __init__(self, name):
		self.name = name
		if self.name == "MainLoop":
			file = "sounds/Mega Man 4 - Toad Man.ogg"
		elif self.name == "Blaze":
			file = "sounds/Raiden - Go to Blazes.ogg"
		pygame.mixer.music.load(file)
		pygame.mixer.music.set_volume(1.0)
	def play(self):
		pygame.mixer.music.play(-1)
	"""
	def update(self):
		if self.name == "Toad":
			if pygame.mixer.music.get_pos() == 65519: #Looping
				pygame.mixer.music.set_pos(35.544)
		elif self.name == "Blaze":
			if pygame.mixer.music.get_pos() == 43 * 1000:
			pygame.mixer.music.set_pos(10)
	"""	
