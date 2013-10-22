# Testing the PLAYER's collisions with the WORLD.

from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera
from code.game import Entity
from code.game import WorldMap


Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

Nut = Entity("nut")
worldmap = WorldMap(2,2)


#########################################################

running = True
while running:
	
	#Loading
	Camera.center = Nut.cbox.center[0], Camera.center[1]
	
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		if Nut.sprite.texture == None:
			Nut.sprite.texture = sf.Texture.from_file\
			("assets/characters/nut/sheet.png")
		else:
			Nut.sprite.texture = None


	Nut.controls(key)
	Nut.physics()
	Nut.collision(worldmap)

	key.reset_all()

	#Videoz
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	worldmap.draw(Camera)
	Nut.draw()
	window.display()