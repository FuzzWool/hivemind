#Run WorldMap inside the main app.
from modules.level_editor import *
from modules.pysfml_game import quit
from modules.pysfml_game import window, sf
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera
from modules.pysfml_game import MySprite

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
		if key.A.held(): Camera.x -= mo.GRID
		if key.D.held(): Camera.x += mo.GRID
		if key.W.held(): Camera.y -= mo.GRID
	if key.S.held(): Camera.y += mo.GRID

#

from modules.worldmap import WorldMap
worldmap = WorldMap()
#########################################################

running = True
# worldmap.load_all()
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	camera_controls()
	worldmap.load_around(*Camera.room_points)

	#Video
	window.view = Camera
	window.clear()
	#
	worldmap.draw()
	#
	window.display()