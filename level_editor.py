from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

from code.game import WorldMap
worldmap = WorldMap(2,2)


###########
from code.level_editor import toolbox
from code.pysfml_game import GRID

#########################################################
from code.pysfml_game import MyMouse

mouse = MyMouse()
TB = toolbox(worldmap) ###


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		print worldmap.rooms[0][0].camera_locks.left
		print TB.camera.all_locks[0][0].left.enabled

	TB.controls(worldmap, Camera, mouse, key) ###

	key.reset_all()

	#Videoa
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	TB.draw(Camera, mouse) ###
	window.view = window.default_view
	TB.static_draw() ###
	#
	window.display()
