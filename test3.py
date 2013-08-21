#Move a camera around the world map.

from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

from modules.game import WorldMap
worldmap = WorldMap()
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed(): worldmap.say_Rooms()

	#Camera movements
	amt = 5
	if key.W.held(): Camera.y -= amt
	if key.S.held(): Camera.y += amt
	if key.A.held(): Camera.x -= amt
	if key.D.held(): Camera.x += amt

	if key.ADD.held(): 		Camera.zoom *= 1.1
	if key.SUBTRACT.held(): Camera.zoom /= 1.1

	#Video
	worldmap.load_around(Camera.room_points, Camera.tile_points)

	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	#
	window.display()