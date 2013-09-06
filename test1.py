from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0


from modules.game import Player
Nut = Player("nut")

from modules.game import WorldMap
worldmap = WorldMap()
#########################################################

running = True
while running:
	
	#Loading
	# Camera.center = Nut.cbox.center
	worldmap\
	.load_around(Camera.room_points, Camera.tile_points)
	
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	# #WIP###
	Nut.handle_controls(key)
	Nut.handle_physics()
	# ###

	#Animation
	Nut.play()

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	Nut.draw()
	Nut.collide_with_WorldMap(worldmap)
	#
	window.display()