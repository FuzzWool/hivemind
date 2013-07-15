import modules as mo
from toolbox import ToolBox
from level_properties import LevelProperties

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

	def __init__(self, Camera, Level):
		self.Camera = Camera
		self.Level = Level
		self.ToolBox = ToolBox(Level, self.cursor_tex)

		#Subclasses
		#Tkinter Menu
		self.LevelProperties = LevelProperties()


	#Pointer Tool###
	def open_LevelProperties(self):
	#Pass the Level's size to the properties
		self.LevelProperties.open()
	###

	def draw(self, mouse):
		#Move the cursor.
		x, y = mouse.grid_position(self.Camera)
		x *= mo.GRID; y *= mo.GRID
		self.cursor.goto = x, y

		#draw Grid externally
		self.cursor.draw()
		self.ToolBox.draw()

	#

	def handle_controls(self, key, mouse):
	#Handles controls specific to the LevelEditor.
	#Uses ToolBox to determine context.
		self.ToolBox.handle_controls\
			(key, mouse, self.Camera, self.Level)
		self.LevelProperties.handle_events()