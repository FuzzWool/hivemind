from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

from code.game import WorldMap
worldmap = WorldMap(4,4)


###########
from code.pysfml_game import MyTexture, MySprite

#ui
from code.pysfml_game import SCREEN_HEIGHT
from code.pysfml_game import GRID


class toolbox:
	
	def __init__(self):
		self.ui = ui()
		self._init_cursor()
		#
		self.tile = tile()

	def draw(self, camera, mouse):
		self.tile.draw()
		self._draw_cursor(camera, mouse)

	def static_draw(self):
		self.ui.draw()

	def controls(self, worldmap, mouse, key):

		self.ui.controls(mouse)

		if not self.ui.is_hovering(mouse):
			if self.ui.selected == "tile":
				self.tile.controls\
				(worldmap, mouse, key, self.cursor)

		if key.L_CTRL.held():
			if key.S.pressed():
				worldmap.save()
	#



	#cursor
	def _init_cursor(self): #init
		cursor_tex \
		= MyTexture("assets/level_editor/cursor.png")
		self.cursor = MySprite(cursor_tex)

	def _draw_cursor(self, camera, mouse): #draw
		x,y = mouse.tile_position
		x += camera.tile_x
		y += camera.tile_y
		self.cursor.tile_position = x,y
		self.cursor.draw()
	#




class ui: #toolbox
#An interface for selecting tools.

	def __init__(self):
		self.selected = None

		self._init_menu()
		self._init_icons()
		

	def controls(self, mouse):

		if self.is_hovering(mouse):
			if mouse.left.pressed():
				self._select(mouse)

	def draw(self):
		window.draw(self.menu)

		for column in self.icons:
			for icon in column:
				if icon != None:
					icon.draw()

	#

	#controls, _init_icons
	def _select(self, mouse=None, x=0, y=0):
		if mouse != None:
			x,y = mouse.tile_position
		self._transparent_icons()
		self.icons[x][y].opaque()
		self.selected = self.icons[x][y].tool


	#controls, _controls
	def is_hovering(self, mouse):
		x,y = mouse.x, mouse.y
		if 0 <= x <= 50\
		and 0 <= y <= SCREEN_HEIGHT:
			return True
		return False

	#

	def _init_menu(self):
		w, h = 50, SCREEN_HEIGHT
		self.menu = sf.RectangleShape((w,h))

	def _init_icons(self):
		self.icons = []

		#Empty
		w, h = 50, SCREEN_HEIGHT
		w, h = int(w/GRID),int(h/GRID)
		for x in range(w):
			self.icons.append([])
			for y in range(h):
				_icon = icon()
				_icon.x, _icon.y = x*GRID, y*GRID
				self.icons[-1].append(_icon)
		#

		#Tools
		self.icons[0][0].tool = "pointer"
		self.icons[1][0].tool = "tile"

		#default
		self._select(x=1,y=0)


	def _transparent_icons(self): #init_icons, select
		for x in self.icons:
			for y in x:
				y.transparent()


class icon(object): #toolbox.ui
	texture = MyTexture("assets/level_editor/toolbox.png")

	def __init__(self):
		self.sprite = MySprite(self.texture)
		self.sprite.clip.set(25,25)
		self.transparent()

	def draw(self):
		self.sprite.draw()

	def transparent(self):
		self.sprite.color = sf.Color(255,255,255,100)
	def opaque(self):
		self.sprite.color = sf.Color(255,255,255,255)


	#
	_tool = None
	@property
	def tool(self): return self._tool
	@tool.setter
	def tool(self, name):
		self._tool = name
		if name == "pointer": self.sprite.clip.use(1,0)
		if name == "tile": self.sprite.clip.use(2,0)


	#

	@property
	def x(self): return self.sprite.x
	@x.setter
	def x(self, x): self.sprite.x = x

	@property
	def y(self): return self.sprite.y
	@y.setter
	def y(self, y):
		self.sprite.y = y



class tile: #toolbox
# Adds and removes tiles to and fro the WorldMap.
# Selects tiles from a tilemap.
	
	def __init__(self):
		self.tilemap = None
		self.selected = "0000"

	def draw(self):
		if self.tilemap != None: self.tilemap.draw()


	def controls(self, worldmap, mouse, key, cursor):

		if not self.is_open:
			if mouse.left.held():
				self.create(worldmap, cursor)
			if mouse.right.held():
				self.remove(worldmap, cursor)

		if key.L_SHIFT.pressed():
			self.open(worldmap, cursor)
		if key.L_SHIFT.released():
			self.close()

		if self.is_open:
			if mouse.left.pressed():
				self.select(cursor)


	####

	#controls

	def create(self, worldmap, cursor):
		x, y = cursor.tile_position
		if worldmap.in_range(x,y):
			worldmap.tiles[x][y].change(self.selected)

	def remove(self, worldmap, cursor):
		x, y = cursor.tile_position
		if worldmap.in_range(x,y):
			worldmap.tiles[x][y].change("____")


	#tilemap

	@property
	def is_open(self): return bool(self.tilemap != None)

	def open(self, worldmap, cursor):
		if self.tilemap == None:
			self.tilemap = self._tilemap(worldmap, cursor)

	def close(self):
		if self.tilemap != None:
			self.tilemap = None

	def select(self, cursor):

		#proportional pos from the tilesheet
		x,y = cursor.tile_position
		ox,oy = self.tilemap.sprite.tile_position
		x -= ox; y -= oy
		x,y = self.tilemap.sprite.keep_in_tile_size(x,y)

		#make key
		x,y = str(x), str(y)
		if len(x) == 1: x = "0"+x
		if len(y) == 1: y = "0"+y

		self.selected = x+y

	##

	class _tilemap:

		def __init__(self, worldmap, cursor):

			#sprite
			x,y = cursor.room_position
			texture = worldmap.rooms[x][y].texture
			self.sprite = MySprite(texture)

			x,y = cursor.tile_position
			self.sprite.tile_position = x,y

		def draw(self):
			self.sprite.draw()

	##


#########################################################
from code.pysfml_game import MyMouse

mouse = MyMouse()
TB = toolbox() ###


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass


	if not key.L_CTRL.held():
		if key.A.held(): Camera.x -= GRID
		if key.D.held(): Camera.x += GRID
		if key.W.held(): Camera.y -= GRID
		if key.S.held(): Camera.y += GRID

	TB.controls(worldmap, mouse, key) ###

	key.reset_all()

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	TB.draw(Camera, mouse) ###
	window.view = window.default_view
	TB.static_draw() ###
	#
	window.display()