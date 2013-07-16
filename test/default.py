import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	#
	window.display()