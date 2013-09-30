#init
from toolbox import ToolBox
#####

import code as mo
from code.pysfml_game import GRID
from code.game import WorldMap


class LevelEditor:
#Alters the data of the WorldMap and all of it's Levels.
#Handles main controls.

	ToolBox = None
	WorldMap = None

	#Sprites
	cursor_tex \
	= mo.MyTexture("assets/level_editor/cursor.png")
	cursor = mo.MySprite(cursor_tex)

	def __init__(self, Camera):
		self.WorldMap = WorldMap()
		self.ToolBox = ToolBox(self.cursor_tex)

	def draw(self, mouse, camera):

		self.WorldMap.draw(camera)

		#Move the cursor.
		x, y = mouse.grid_position(camera)
		x *= mo.GRID; y *= mo.GRID
		self.cursor.goto = x, y

		self.cursor.draw()
		self.ToolBox.draw()

	#

	#CONTROLS
	def camera_controls(self, key, Camera):
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

	def handle_controls(self, key, mouse, camera):
	#Forwards a level for editing to the ToolBox.
	#Selects the level based on what is currently
	#being highlighted.

		self.ToolBox.ui_controls(mouse)

		#Event conditions
		level_selected = None

		mouse_x, mouse_y = mouse.position(camera)
		for x in self.WorldMap.rooms:
			for Room in x:
				x1 = Room.tiles_x*GRID
				y1 = Room.tiles_y*GRID
				x2 = x1 + Room.tiles_w*GRID
				y2 = y1 + Room.tiles_h*GRID

				if (x1 < mouse_x < x2)\
				and (y1 < mouse_y < y2):
					level_selected = Room
					break

		#Events

		#Save the WorldMap and all the levels.
		if key.L_CTRL.held():
			if key.S.pressed():
				self.WorldMap.save()

		#If a Level's been selected...
		if level_selected != None:

			self.ToolBox.level_controls\
				(key, mouse, camera, level_selected)
	#
