import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MyMouse

#Double-clicking.

MOUSE = MyMouse()
running = True
while running:
	#Logic
	if quit(): running = False
	if MOUSE.left.double_pressed():
		print "double"

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	#
	window.display()