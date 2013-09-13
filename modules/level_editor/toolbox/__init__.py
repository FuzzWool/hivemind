from modules.pysfml_game import MyTexture, MySprite
from modules.pysfml_game import SCREEN_HEIGHT
from modules.pysfml_game import GRID
from modules.pysfml_game import sf

from tile import Tile
from pointer import Pointer

class ToolBox:
#Event handling for all of the tools.
	def __init__(self, cursor_tex):
		self.UI = _ui()
		
		self.Pointer = Pointer()
		self.Tile = Tile(cursor_tex)

	#UI is drawn externally so that it stays in place.
	def draw(self):
		self.Tile.draw()


	# CONTROLS

	def ui_controls(self, mouse):
	#Checked constantly.
		hovering_toolbox = bool(mouse.x < self.UI.w)

		if hovering_toolbox:
			if mouse.left.pressed():
				self.UI.select_tool(mouse)

		self.Pointer.LevelProperties.handle_events()


	def level_controls(self, key, mouse, camera, Level):
	#Only checked when a level is highlighted.
	#Level-specific tools.
		tool = self.UI.selected_tool
		hovering_toolbox = bool(mouse.x < self.UI.w)

		hovering_level = False
		x, y = mouse.position(camera)
		lx = Level.x*GRID; lw = lx + Level.w*GRID
		ly = Level.y*GRID; lh = ly + Level.h*GRID
		if (lx < x < lw)\
		and (ly < y < lh):
			hovering_level = True

		if tool == "pointer":
			if hovering_level:
				if mouse.left.double_clicked():
					self.Pointer.LevelProperties.open(Level)

		if tool == "tile":
			grid_pos = mouse.grid_position(camera)
			if not hovering_toolbox:

				if key.L_CTRL.held():
					if mouse.left.pressed():
						self.Tile.Selector.open\
						(Level, grid_pos)
				else:
					if mouse.left.held():
						self.Tile.place(Level, grid_pos)
					if mouse.right.held():
						self.Tile.remove(Level, grid_pos)
					if mouse.left.pressed():
						self.Tile.Selector.select\
						(Level, grid_pos)
					if mouse.left.released():
						self.Tile.Selector.close()

class _ui:
#The side panel for selecting tools.
#May return a selected tool for event handling.
	b_sprite = None
	tex = MyTexture("img/level_editor/toolbox.png")

	_selected_tool = (1, 0)
	tools = []
	tools_sprites = []


	@property
	def w(self): return self.b_sprite.box.w

	@property
	def selected_tool(self):
		x, y = self._selected_tool
		return self.tools[x][y]

	def __init__(self):
		self._create_graphics()


	def _create_graphics(self):
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
			self.tools_sprites[1][0].color \
			= sf.Color(255,255,255,255)

	def draw(self):
		self.b_sprite.box.draw()
		for x in self.tools_sprites:
			for y in x:
				y.draw()

	#

	def select_tool(self, Mouse):
	#Select the tool which's been clicked.

		x, y = Mouse.x / GRID, Mouse.y / GRID
		if self.tools[x][y] != None:
			#Dull the old one.
			x, y = self._selected_tool
			self.tools_sprites[x][y].color \
			= sf.Color(255,255,255,125)

			x, y = Mouse.x / GRID, Mouse.y / GRID
			self._selected_tool = (x, y)

			#Brighten the new one.
			self.tools_sprites[x][y].color \
			= sf.Color(255,255,255,255)