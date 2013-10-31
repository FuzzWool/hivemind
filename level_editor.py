from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera
from code.pysfml_game import MyMouse

from code.game import WorldMap
from code.game import entities

from code.level_editor import toolbox
##########################################

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

###
x,y = 4, 30
worldmap = WorldMap(x,y)
entities = entities(None, worldmap, None)
###

mouse = MyMouse()
toolbox = toolbox(worldmap, entities) ###

##########################################
running = True
while running:

	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	toolbox.controls\
	(entities, worldmap, Camera, mouse, key)
	key.reset_all()

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	entities.draw(Camera) ###
	toolbox.draw(Camera, mouse)
	window.view = window.default_view
	toolbox.static_draw()
	#
	window.display()
