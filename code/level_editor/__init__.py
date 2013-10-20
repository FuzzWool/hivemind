from code.pysfml_game import MyTexture, MySprite

#ui
from code.pysfml_game import SCREEN_HEIGHT
from code.pysfml_game import GRID
from code.pysfml_game import sf
from code.pysfml_game import window

class toolbox:
	
	def __init__(self, worldmap):
		self.ui = ui()
		self._init_cursor()
		#
		self.pointer = pointer()
		self.tile = tile()
		self.camera = camera(worldmap)

	def draw(self, camera, mouse):
		self._move_cursor(camera, mouse)

		if self.ui.selected == "tile":
			self.tile.draw()
			self.cursor.draw()
		if self.ui.selected == "camera":
			self.camera.draw(camera)


	def static_draw(self):
		self.ui.draw()

	def controls(self, worldmap, mouse, key):

		self.ui.controls(mouse)

		if not self.ui.is_hovering(mouse):

			if self.ui.selected == "pointer":
				self.pointer.controls\
				(worldmap, mouse, self.cursor)
			
			if self.ui.selected == "tile":
				self.tile.controls\
				(worldmap, mouse, key, self.cursor)

			if self.ui.selected == "camera":
				self.camera.controls\
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

	def _move_cursor(self, camera, mouse): #draw
		x,y = mouse.tile_position
		x += camera.tile_x
		y += camera.tile_y
		self.cursor.tile_position = x,y
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
		self.icons[0][1].tool = "camera"

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
		if name == "camera": self.sprite.clip.use(3,0)

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
		self.lp1 = \
		self.LevelProperties_1(self.root, Level)

		def save():
			tileset = self.lp1.tileset.get()
			Level.change_texture(tileset)
			self.root.destroy()

		self.butt = \
		self.ConfirmButtons(self.root, save)
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
			frame = Frame(self, relief=RAISED,\
			 borderwidth=1)
			frame.pack(fill=BOTH, expand=1)

			Bclose = Button(self, text="Nah.",\
			 command=self.parent.destroy)
			Bclose.pack(side=RIGHT, padx=5, pady=5)
			Bok = Button(self, text="Okay!", command=arg)
			Bok.pack(side=RIGHT)

			self.pack(fill=BOTH, expand=1)





############################
############################
############################
############################
############################
############################


from code.pysfml_game import RENDER_HEIGHT, RENDER_WIDTH


class camera:
#WIP - Created for each room.
#Rendered ON-THE-FLY.
	
	def __init__(self, worldmap):
	#Create locks for every room of the worldmap.
		self.worldmap = worldmap

		self.all_locks = []
		for x in range(self.worldmap.rooms_w):
			self.all_locks.append([])

			for y in range(self.worldmap.rooms_h):
				lock = locks(x,y)
				self.all_locks[-1].append(lock)


	def draw(self, camera):
		for column in self.all_locks:
			for locks in column:	
				locks.draw(camera)


	def controls(self, worldmap, mouse, cursor):
	#Press the locks in order to toggle them. 
		
		#find which lock to select
		x,y = cursor.room_position

		if 0 <= x < worldmap.rooms_h\
		and 0 <= y < worldmap.rooms_w:
			
			self.all_locks[x][y].controls\
			(mouse, cursor)



#
class locks:
#Sets camera locks for each side of a single room.

	def __init__(self, room_x, room_y):
		args = room_x, room_y

		#sides
		self.left = side("left", *args)
		self.right = side("right", *args)
		self.up = side("up", *args)
		self.down = side("down", *args)
		#
		self.sides \
		= [self.left, self.right, self.up, self.down]


		#lock
		self.lock = lock(*args)


	def draw(self, camera):
		for side in self.sides:
			side.draw(camera)
		self.lock.draw(camera)


	#

	def controls(self, mouse, cursor):

		pressed = mouse.left.pressed()

		#Toggle a SIDE.
		#Enable the lock if any are enabled.
		#Disable the lock if all are disabled.
		any_enabled = False

		for side in self.sides:
			if side.sprite != None:
				if pressed:
					if cursor.in_bounds(side.sprite):
						side.toggle()

				if side.enabled:
					self.lock.enable()
					any_enabled = True
		
		if pressed:
			if any_enabled:
				self.lock.enable()
			else:
				self.lock.disable()


		#Toggle the LOCK.
		#Enables all sides if enabled.
		#Disables all sides if disabled.
		if pressed:

			if self.lock.sprite != None:
				if cursor.in_bounds(self.lock.sprite):
					self.lock.toggle()

					for side in self.sides:
						if self.lock.enabled:
							side.enable()
						else:
							side.disable()


from code.pysfml_game import MySprite_Loader
##
class side(MySprite_Loader):
#A conditions and configurations for loading the
#side sprites.

	def __init__ (self, pos, room_x, room_y):
		MySprite_Loader.__init__(self)
		self.init_position(pos, room_x, room_y)
		self.init_toggle()


	#TOGGLE

	def init_toggle(self): #init
		self.enabled = False
		self.enable()

	def toggle(self):
		if self.enabled: self.disable()
		else: self.enable()

	disable_c = sf.Color(0,0,0,100)
	enable_c = sf.Color(255,255,255,255)
	def disable(self):
		self.enabled = False
		if self.sprite != None:
			self.sprite.color = self.disable_c
	def enable(self):
		self.enabled = True
		if self.sprite != None:
			self.sprite.color = self.enable_c


	#POSITION

	x_texture = MyTexture\
	("assets/level_editor/camera/x_side.png")
	y_texture = MyTexture\
	("assets/level_editor/camera/y_side.png")

	def init_position(self, pos, room_x, room_y): #init
		self.pos = pos
		self.room_x, self.room_y = room_x, room_y


	def load(self, args=None):
		pos = self.pos
		room_x, room_y = self.room_x, self.room_y

		if pos in ("left","right"):
			self.sprite = MySprite(self.x_texture)

			if pos == "left":
				pass

			if pos == "right":
				self.sprite.clip.flip_horizontal()
				self.sprite.x = RENDER_WIDTH - GRID


		if pos in ("up","down"):
			self.sprite = MySprite(self.y_texture)

			if pos == "up":
				pass

			if pos == "down":
				self.sprite.clip.flip_vertical()
				self.sprite.y = RENDER_HEIGHT - GRID

		self.sprite.x += room_x*RENDER_WIDTH
		self.sprite.y += room_y*RENDER_HEIGHT

		#Render the sprite
		self.toggle(); self.toggle()


from code.pysfml_game import MySprite_Loader
##
class lock(MySprite_Loader):
	
	def __init__(self, room_x, room_y):
		self._init_position(room_x, room_y)
		self._init_toggle()


	#PUBLIC

	def _init_toggle(self):
		self.enabled = True
		self.enable()

	def toggle(self):
		if self.enabled: self.disable()
		else: self.enable()

	def disable(self):
		self.enabled = False
		if self.sprite != None:
			self.sprite.clip.use(1,0)
	def enable(self):
		self.enabled = True
		if self.sprite != None:
			self.sprite.clip.use(0,0)

	#

	texture = MyTexture\
	("assets/level_editor/camera/lock.png")


	def _init_position(self, room_x, room_y):
		self.sprite = None
		self.room_x, self.room_y = room_x, room_y


	def load(self, args=None):
		s = MySprite(self.texture)
		s.clip.set(100,120)
		s.center = RENDER_WIDTH/2, RENDER_HEIGHT/2
		s.x += self.room_x*RENDER_WIDTH
		s.y += self.room_y*RENDER_HEIGHT

		self.sprite = s

		self.toggle(); self.toggle() #render the sprite