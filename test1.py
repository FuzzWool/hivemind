#Run WorldMap inside the main app.
from modules.level_editor import *
from modules.pysfml_game import quit
from modules.pysfml_game import window, sf
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0
from modules.worldmap import WorldMap

worldmap = WorldMap()
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
	window.view = Camera
	window.clear(sf.Color(255, 0, 255))
	#
	worldmap.draw()
	#
	window.display()