from modules.pysfml_game import MyTexture, MySprite
from modules.pysfml_game import SCREEN_HEIGHT
from modules.pysfml_game import GRID
from modules.pysfml_game import sf

class ToolBox:
#Used for selecting a tool.
#The tool is used then by LevelEditor to change the
#user's actions.
	b_sprite = None
	tex = MyTexture("img/level_editor/toolbox.png")

	_selected_tool = (0, 0)
	tools = []
	tools_sprites = []


	@property
	def w(self): return self.b_sprite.box.w

	@property
	def selected_tool(self):
		x, y = self._selected_tool
		return self.tools[x][y]

	def __init__(self):
	#Create the graphics.
		
		#Create the base sprite.
		self.b_sprite = MySprite(None)
		self.b_sprite.box.size = 50, SCREEN_HEIGHT

		#Create the empty slots.
		h = self.b_sprite.box.h / GRID
		w = self.b_sprite.box.w / GRID

		for x in range(w):
			self.tools_sprites.append([])
			self.tools.append([])
			for y in range(h):
				g = MySprite(self.tex)
				g.clip.set(25, 25)
				g.clip.use(0, 0)
				g.goto = GRID*x, GRID*y
				g.color = sf.Color(255,255,255,125)

				self.b_sprite.children.append(g)
				self.tools_sprites[x].append(g)
				self.tools[x].append(None)

		#Define tools already made.
		self.tools_sprites[0][0].clip.use(1, 0)
		self.tools[0][0] = "pointer"

		self.tools_sprites[1][0].clip.use(2, 0)
		self.tools[1][0] = "tile"

	def draw(self):
		self.b_sprite.box.draw()
		for x in self.tools_sprites:
			for y in x:
				y.draw()

	#

	def select_tool(self, Mouse):
	#Select the tool which's been clicked.
		#Dull the old one.
		x, y = self._selected_tool
		self.tools_sprites[x][y].color \
		= sf.Color(255,255,255,125)

		x, y = Mouse.x / GRID, Mouse.y / GRID
		if self.tools[x][y] != None:
			self._selected_tool = (x, y)

			#Brighten the new one.
			self.tools_sprites[x][y].color \
			= sf.Color(255,255,255,255)