import pygame
import Settings
from Settings import *


class EightCrypt(object):
	def encrypt(self, text):
		output = ""
		count = 0
		for letter in text:
			num = ord(letter)
			for i in range(0, num):
				output = output + "8"
			output += " "
		return output
					
	def decrypt(self, text):
		output = ""
		count = 0
		for letter in text:
			if letter == "8":
				count += 1
			else:
				output += chr(count)
				count = 0
		return output		
				
	def read(self, filename):
		file = open(filename,'r')
		lines = []
		count = 0
		for line in file:
			lines.append(self.decrypt(line))
			count += 1
		return lines
			
	def write(self, filename, text):
		file = open(filename,'w')
		for line in text:
			file.write(self.encrypt(line) + "\n")

