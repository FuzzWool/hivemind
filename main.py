#Run WorldMap inside the main app.
from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

from code.game import WorldMap
worldmap = WorldMap()
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	#
	window.display()