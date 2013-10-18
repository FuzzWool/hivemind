from code.pysfml_game import MyTexture, MySprite

#ui
from code.pysfml_game import SCREEN_HEIGHT
from code.pysfml_game import GRID
from code.pysfml_game import sf
from code.pysfml_game import window

class toolbox:
	
	def __init__(self):
		self.ui = ui()
		self._init_cursor()
		#
		self.pointer = pointer()
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

			if self.ui.selected == "pointer":
				self.pointer.controls\
				(worldmap, mouse, self.cursor)

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







############################
############################
############################
############################
############################
############################










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















############################
############################
############################
############################
############################
############################







class pointer:

	def __init__(self):
		self.level_properties = _LevelProperties()

	def controls(self, worldmap, mouse, cursor):
		if mouse.left.double_pressed():
			self._open(worldmap, cursor)
		self._handle()

	#

	def _open(self, worldmap, cursor):
		x,y = cursor.room_position
		room = worldmap.rooms[x][y]
		self.level_properties.open(room)

	def _handle(self):
		self.level_properties.handle_events()


from Tkinter import Tk, Frame, Button
from Tkinter import BOTH

from Tkinter import Entry, Label
from Tkinter import N, E, S, W
from Tkinter import INSERT
from Tkinter import LEFT, RIGHT, TOP, BOTTOM
from Tkinter import X, Y
from Tkinter import RAISED

class _LevelProperties:
#Opens and alters the properties of a level,
#with a windows form.
	root = None

	def open(self, Level):
	#Opens the properties window.
	#Passes over the values.
		self.root = Tk()
		self.root.wm_title(Level.texture_name)
		self.lp1 = self.LevelProperties_1(self.root, Level)

		def save():
			tileset = self.lp1.tileset.get()
			Level.change_texture(tileset)
			self.root.destroy()

		self.butt = self.ConfirmButtons(self.root, save)
		self.lp1.focus_force()
		self.root.mainloop()

	def handle_events(self):
	#Updates only windows within existence.
		if self.root != None:
			if len(self.root.children) >= 1:
				tkinter_open = True
			else:
				tkinter_open = False
		else:
			tkinter_open = False

		if tkinter_open:
			if len(self.root.children) >= 1:
				self.root.update()

	#

	class MyFrame(Frame):
	#Override me!
		def __init__(self, parent, arg=None):
			Frame.__init__(self, parent)
			self.parent = parent
			self.initUI(arg)

		def initUI(self, arg=None):
		#Replace me!
			pass

	class LevelProperties_1(MyFrame):

		def initUI(self, Level):
		#Level Properties title
			# name = Level.name
			tileset = Level.texture_name

			entry_row = 1
			Ltileset = Label(self, text="Tileset")
			Ltileset.grid(row=entry_row, column=0)
			Etileset = Entry(self)
			Etileset.grid(row=entry_row, column=1)
			Etileset.insert(INSERT, tileset)

			self.pack(fill=BOTH, expand=1)

			self.tileset = Etileset

	class ConfirmButtons(MyFrame):

		def initUI(self, arg=None):
			frame = Frame(self, relief=RAISED, borderwidth=1)
			frame.pack(fill=BOTH, expand=1)

			Bclose = Button(self, text="Nah.", command=self.parent.destroy)
			Bclose.pack(side=RIGHT, padx=5, pady=5)
			Bok = Button(self, text="Okay!", command=arg)
			Bok.pack(side=RIGHT)

			self.pack(fill=BOTH, expand=1)