from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

from modules.level import Level
level = Level("aa", 0, 0)
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	level.load_around\
	(*Camera.tile_points)

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	level.draw()
	#
	window.display()