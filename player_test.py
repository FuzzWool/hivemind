from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key


############
from code.game import Entity
from code.game import WorldMap
from code.game import GameCamera
from code.game import entities
from code.game import Timer

Camera = GameCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0
Nut = Entity("nut")
Camera.focus = Nut.cbox

timer = Timer()

x,y = 4,30
worldmap = WorldMap(x,y)
entities = entities(Nut, worldmap, timer) ####

############


running = True
while running:

	#LOGIC
	#
	#window
	if quit(): running = False
	if key.RETURN.held():
		pass

	#entity
	Nut.controls(key)
	Nut.physics()
	Nut.collision(worldmap)

	entities.react() ####


	#key
	key.reset_all()


	#VIDEO
	#
	#camera
	Camera.process_movement(worldmap)
	window.view = Camera
	
	#drawing
	window.clear(sf.Color(255, 200, 200))
	worldmap.draw(Camera)
	entities.draw(Camera) ####
	Nut.draw()

	#static drawing
	old_pos = Camera.position
	Camera.position = 0,0
	window.view = Camera
	timer.draw()
	Camera.position = old_pos

	window.display()