from EightCrypt import *
e = EightCrypt()
a = e.read("highscores.txt")
for i in range(0,len(a)):
	print "{0:1d}.\'{1:1s}\'".format(i, a[i])
