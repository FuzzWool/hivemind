from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera
from code.pysfml_game import MyMouse

from code.game import WorldMap

from code.level_editor import toolbox

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

worldmap = WorldMap(2,2)

mouse = MyMouse()
toolbox = toolbox(worldmap) ###

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	toolbox.controls(worldmap, Camera, mouse, key) ###
	key.reset_all()

	#Videoa
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	toolbox.draw(Camera, mouse) ###
	window.view = window.default_view
	toolbox.static_draw() ###
	#
	window.display()
