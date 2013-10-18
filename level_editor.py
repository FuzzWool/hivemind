from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

from code.game import WorldMap
worldmap = WorldMap(4,4)


###########
from code.level_editor import toolbox
from code.pysfml_game import GRID

#########################################################
from code.pysfml_game import MyMouse

mouse = MyMouse()
TB = toolbox() ###


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass


	if not key.L_CTRL.held():
		if key.A.held(): Camera.x -= GRID
		if key.D.held(): Camera.x += GRID
		if key.W.held(): Camera.y -= GRID
		if key.S.held(): Camera.y += GRID

	TB.controls(worldmap, mouse, key) ###

	key.reset_all()

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	TB.draw(Camera, mouse) ###
	window.view = window.default_view
	TB.static_draw() ###
	#
	window.display()