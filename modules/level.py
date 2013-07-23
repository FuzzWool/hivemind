import modules as mo
from modules.pysfml_game import MySprite
from modules.pysfml_game import GRID
from modules.pysfml_game import sf
from modules.pysfml_game import ROOM_WIDTH, ROOM_HEIGHT

class Level(object):
	name = ""
	texture_name = ""
	texture = "loaded from the first level file line"
	level = []; tiles = []
	alphabet = ["a","b","c","d","e","f","g",\
	 "h","i","j","k","l","m","n","o","p","q",\
	 "q","r","s","t","u","v","w","x","y","z"]

 	#Properties (size, position)
	_x, _y = 0, 0

	@property
	def x(self): return self._x
	@x.setter
	def x(self, arg):
		self._x = arg

	@property
	def y(self): return self._y
	@y.setter
	def y(self, arg):
		self._y = arg

	@property
	def w(self): return len(self.level)

	@property
	def h(self): return len(self.level[0])

	@property
	def room_x(self): return int(self.x*GRID / ROOM_WIDTH)
	@room_x.setter
	def room_x(self, arg): self.x = arg*(ROOM_WIDTH/GRID)

	@property
	def room_y(self): return int(self.y*GRID / ROOM_HEIGHT)
	@room_y.setter
	def room_y(self, arg): self.y = arg*(ROOM_HEIGHT/GRID)

	@property
	def room_w(self): return int(self.w*GRID / ROOM_WIDTH)
	@property
	def room_h(self): return int(self.h*GRID / ROOM_HEIGHT)
	#

	def __init__ (self, level_dir, room_x=0, room_y=0):
	#Grabs level data and creates tiles.

		self.room_x, self.room_y = room_x, room_y
		self.level = self._load_level(level_dir)
		self.tiles = self._initialize_tiles(self.level)
		# self.tiles = self._make_all_tiles(self.level)


	def change_tile(self, pos, clip):
	#Changes a tile, updates the level and tiles.

		def make_tile(pos=(), clip=()):
		#Make a new tile. Requires filler to be in place.

			if clip == "__":
				return self.empty_tile(pos)
			#
			sprite = mo.MySprite(self.texture)
			sprite.clip.set(mo.GRID, mo.GRID)
			cx = self.alphabet.index(clip[0])
			cy = self.alphabet.index(clip[1])
			sprite.clip.use(cy, cx)
			x, y = pos[0]*mo.GRID, pos[1]*mo.GRID
			# print self.room_x, self.room_y
			x += self.x*GRID; y += self.y*GRID
			sprite.goto = x, y
			return sprite

		x, y = pos[0], pos[1]
		tile = make_tile(pos, clip)
		self.tiles[x][y] = tile
		self.level[x][y] = clip

	def empty_tile(self, pos=(), clip=()):
	#I exist entirely for Elevel's sake.
		return None

	def draw(self):
		for x in self.tiles:
			for y in x:
				if y != None:
					y.draw()


#	LOADING DATA

	def _load_level(self, level_dir):
	#Loads and formats the level for usage.

		def get_level(level_dir):
		#Grab level data from text file.
			self.name = level_dir
			level_dir = "outside/levels/%s.txt" % level_dir
			
			try: #loading the file...
				f = open(level_dir)
				level = f.read()
				f.close()
			except: #If that fails, use a generic template.
				level = "_template"

			return level

		def grab_texture(level):
		#Load the texture from the first level data line.
			#Grab and remove the texture line.
			self.texture_name = level.split("\n")[0]
			tex_dir = "img/tilemaps/%s.png" \
			% self.texture_name
			self.texture = mo.texture(tex_dir)

			lvl = ""
			for line in level.split("\n")[1:]:
				lvl += str(line) + "\n"

			return lvl[:-1]

		def format_level(level):
		#The level is now in an [x][y] format.
			rows = level.split("\n")
			format = []
			i = 0
			while i < len(rows[0])-1:
				format.append([c[i]+c[i+1] for c in rows])
				i += 2
			return format

		def room_off_level(level):
		#The level should be room-sized.
			def room_w():
				room = mo.ROOM_WIDTH/mo.GRID
				w = room
				while w < len(level)-1:
					w += room
				return w
			def room_h(x):
				room = mo.ROOM_HEIGHT/mo.GRID
				h = room
				while h < len(level[0])-1:
					h += room
				return h
			#
			level_w = lambda: len(level)
			level_h = lambda x: len(level[x])

			#Append pre-existing columns.
			x = 0
			while x < room_w():

				#Add new column if needed.
				if x >= level_w():
					level.append([])

				y = level_h(x)
				while y < room_h(x):
					level[x].append("__")
					y += 1
				y = 0
				x += 1

			return level

		level = get_level(level_dir)
		level = grab_texture(level)
		level = format_level(level)
		level = room_off_level(level)
		return level


#	TILE CREATION

	def _initialize_tiles(self, level):
	#Make spaces for the tiles to reside in.
		tiles = []
		fill = [None for y in level[0]]
		while len(tiles) < len(level):
			tiles.append(fill)
		return [tile[:] for tile in tiles]


	def _make_all_tiles(self, level):
	#Make ALL of the tiles in the Level.
		for ix, x in enumerate(level):
			for iy, y in enumerate(x):
				y = "aa"
				self.change_tile((ix, iy), y)
		return self.tiles


	def load_around(self, x1, y1, x2, y2):
	#Load only the tiles within a certain AREA.

		def keep_in_bounds(x=0, y=0):
			if self.w < x: x = self.w
			if self.h < y: y = self.h
			if x < 0: x = 0
			if y < 0: y = 0
			return x, y

		x1 -= self.x; x2 -= self.x
		y1 -= self.y; y2 -= self.y
		x1, y1 = keep_in_bounds(x1, y1)
		x2, y2 = keep_in_bounds(x2, y2)

		for x in range(self.w):
			for y in range(self.h):

				#Make a tile within the area.
				if  x1 <= x <= x2\
				and y1 <= y <= y2:
					if self.tiles[x][y] == None\
					and self.level[x][y] != "__":

						self.change_tile((x, y),\
						 self.level[x][y])

				#Remove any tiles outside of the area.
				if x < x1 or x2 < x\
				or y < y1 or y2 < y:

					self.tiles[x][y] = None

# DEBUGGING

	@property
	def tiles_loaded(self):
		loaded = []
		for x in self.tiles:
			for y in x:
				if y != None:
					loaded.append(y)
		return loaded

	def say_tiles(self):
		total = self.w * self.h
		loaded = len(self.tiles_loaded)

		string = "%s loaded (%s/%s) tiles."\
		% (self.name, loaded, total)
		print string