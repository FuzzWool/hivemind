#Testing MOVING AROUND the WORLDMAP.

import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MyCamera

from code.game import WorldMap


Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0,0


worldmap = WorldMap(4,4)
print "WorldMap INITIALIZED."

#########################################################

running = True
while running:
	
	#LOGIC
	if quit(): running = False
	if key.RETURN.pressed():
		room = worldmap.rooms[0][0]
		tile = room.tiles[2][1]


	amt = 5
	if key.LEFT.held(): Camera.x -= amt
	if key.RIGHT.held(): Camera.x += amt
	if key.UP.held(): Camera.y -= amt
	if key.DOWN.held(): Camera.y += amt

	#VIDEO
	window.clear(sf.Color.WHITE)
	window.view = Camera

	#
	worldmap.draw(Camera)
	#


	window.display()