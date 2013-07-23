#Run WorldMap inside the main app.
from modules.level_editor import *
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

#
def camera_controls():
	if key.L_CTRL.held():
		#Zoom Camera
		if key.ADD.pressed(): Camera.zoom *= 2
		if key.SUBTRACT.pressed(): Camera.zoom /= 2

	elif key.L_SHIFT.held():
		#Move Camera - Snap to Room
		if key.A.pressed(): Camera.room_x -= 1
		if key.D.pressed(): Camera.room_x += 1
		if key.W.pressed(): Camera.room_y -= 1
		if key.S.pressed(): Camera.room_y += 1

	else:
		#Move Camera
		if key.A.held(): Camera.x -= 5
		if key.D.held(): Camera.x += 5
		if key.W.held(): Camera.y -= 5
	if key.S.held(): Camera.y += 5

#

from modules.worldmap import WorldMap
worldmap = WorldMap()
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		worldmap.say_Rooms()

	camera_controls()
	worldmap.load_around\
	(Camera.room_points, Camera.tile_points)

	#Video
	window.view = Camera
	window.clear()
	#
	worldmap.draw()
	#
	window.display()