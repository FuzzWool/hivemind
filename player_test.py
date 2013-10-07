# Testing the PLAYER's collisions with the WORLD.


from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0


from code.game import Player
Nut = Player("nut")

from code.game import WorldMap
worldmap = WorldMap(2,2)


#########################################################

running = True
while running:
	
	#Loading
	Camera.center = Nut.cbox.center[0], Camera.center[1]
	
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		worldmap.tiles[12][10].change("0100")


	Nut.handle_controls(key)
	Nut.handle_physics()
	Nut.collide_with_WorldMap(worldmap)

	key.reset_all()

	#Animation
	Nut.play()

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	worldmap.draw(Camera)
	Nut.draw()
	window.display()