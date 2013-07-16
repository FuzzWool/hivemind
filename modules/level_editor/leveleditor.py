import modules as mo
from toolbox import ToolBox
from modules.level_editor import ELevel

class LevelEditor:
#Alters the data of the currently loaded level.
#Will eventually hold and alter levels en mass.

	#External classes.
	Camera = None
	Level = None

	#Internal classes.
	ToolBox = None

	#Sprites
	cursor_tex = mo.texture("img/level_editor/cursor.png")
	cursor = mo.MySprite(cursor_tex)

	def __init__(self, Camera):
		self.Camera = Camera
		# self.Level = Level
		# self.ToolBox = ToolBox(Level, self.cursor_tex)

	def draw(self, mouse):

		for Level in self.Levels:
			Level.draw()

		#Move the cursor.
		x, y = mouse.grid_position(self.Camera)
		x *= mo.GRID; y *= mo.GRID
		self.cursor.goto = x, y

		self.cursor.draw()
		# self.ToolBox.draw()

		#

	#

	def handle_controls(self, key, mouse):
	#Handles controls specific to the LevelEditor.
	#Uses ToolBox to determine context.
		pass
		# self.ToolBox.handle_controls\
		# 	(key, mouse, self.Camera, self.Level)

	#

	# WORLDMAP
	# Handles glueing the individual levels together.

	WorldMap = [["level"],["x"],["y"]]
	Levels = [["Level"]]

	def load_WorldMap(self):
	#For each level, Load the...
	#Filename and x/y Coordinates

		#Load
		f = open("outside/levels/WorldMap.txt")
		WorldMap = f.read()
		f.close()

		#Format [[level][x][y]]
		WorldMap = WorldMap.split("\n")
		wm = []
		for entry in WorldMap:
			formatted_entry = entry.split(",")
			wm.append(formatted_entry)
		self.WorldMap = [entry[:] for entry in wm]

		#Load and position the Levels
		self.Levels = []
		for entry in self.WorldMap:
			Level = ELevel(entry[0])
			Level.room_x = int(entry[1])
			Level.room_y = int(entry[2])
			self.Levels.append(Level)


	def save_WorldMap(self):
		pass