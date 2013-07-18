#init
from elevel import *
from toolbox import *
#####

import modules as mo
from toolbox import ToolBox
from modules.worldmap import WorldMap
from modules.pysfml_game import GRID

class LevelEditor:
#Alters the data of the currently loaded level.
#Will eventually hold and alter levels en mass.

	#External classes.
	Camera = None
	Level = None

	#Internal classes.
	ToolBox = None
	WorldMap = None

	#Sprites
	cursor_tex = mo.texture("img/level_editor/cursor.png")
	cursor = mo.MySprite(cursor_tex)

	def __init__(self, Camera):
		self.Camera = Camera
		self.WorldMap = WorldMap()
		self.ToolBox = ToolBox(self.cursor_tex)

	def draw(self, mouse):

		self.WorldMap.draw()

		#Move the cursor.
		x, y = mouse.grid_position(self.Camera)
		x *= mo.GRID; y *= mo.GRID
		self.cursor.goto = x, y

		self.cursor.draw()
		self.ToolBox.draw()

		#

	#

	def handle_controls(self, key, mouse, camera):
	#Forwards a level for editing to the ToolBox.
	#Selects the level based on what is currently
	#being highlighted.

		self.ToolBox.ui_controls(mouse)

		#Event conditions
		level_selected = None

		mouse_x, mouse_y = mouse.position(camera)
		for Level in self.WorldMap.Levels:
			x1, y1 = Level.x*GRID, Level.y*GRID
			x2, y2 = x1 + Level.w*GRID, y1 + Level.h*GRID

			if (x1 < mouse_x < x2)\
			and (y1 < mouse_y < y2):
				level_selected = Level
				break

		#Events
		#If a Level's been selected...
		if level_selected != None:
			
			self.ToolBox.level_controls\
				(key, mouse, self.Camera, level_selected)

			#Save the level.
			if key.L_CTRL.held():
				if key.S.pressed():
					Level.save()

		#Double-clicking an empty space makes a new level.
		else:
			if mouse.left.double_clicked():
				x, y = mouse.room_position(camera)
				self.WorldMap.load_Level("new", x, y)

		#Save the WorldMap and all the levels.
		if key.L_SHIFT.held():
			if key.L_CTRL.held():
				if key.S.pressed():
					self.WorldMap.save()

	#
