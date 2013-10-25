from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key

from code.game import Entity
from code.game import WorldMap
from code.game import GameCamera


Camera = GameCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

Nut = Entity("nut")
worldmap = WorldMap(3,3)

Camera.focus = Nut.cbox

running = True
while running:
		
	#LOGIC
	#
	#window
	if quit(): running = False
	if key.RETURN.pressed():
		if Nut.sprite.texture == None:
			Nut.sprite.texture = sf.Texture.from_file\
			("assets/characters/nut/sheet.png")
		else:
			Nut.sprite.texture = None

	#entity
	Nut.controls(key)
	Nut.physics()
	Nut.collision(worldmap)

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
	Nut.draw()
	window.display()