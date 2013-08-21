from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import GRID
from modules.pysfml_game import ROOM_WIDTH, ROOM_HEIGHT

class Room(object):
	name = ""
	texture_name = ""
	texture = "loaded from the first room file line"
	data = []; tiles = []
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
	def w(self): return len(self.data)

	@property
	def h(self): return len(self.data[0])

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

	def __init__ (self, room_dir, room_x=0, room_y=0):
	#Grabs Room data and creates tiles.

		self.room_x, self.room_y = room_x, room_y

		self.data = self._load_room(room_dir)
		# self.data = [["aa"]]
		# self.texture = MyTexture("img/tilemaps/level.png")
		
		self.tiles = self._initialize_tiles(self.data)
		# self.tiles = self._make_all_tiles(self.data)

		#Collisions.
		self.collision = collision(self)
		# self.collision.make_bounds()
		self.collision.filler()


	#	WIP - TILE CREATION

	class Tile:
		data = "__"
		sprite = None

	#

	def change_tile(self, pos, clip):
	#Changes a tile, updates the Room and tiles.

		def make_tile(pos=(), clip=()):
		#Make a new tile. Requires filler to be in place.

			if clip == "__":
				return self.empty_tile(pos)
			#
			sprite = MySprite(self.texture)
			sprite.clip.set(GRID, GRID)
			cx = self.alphabet.index(clip[0])
			cy = self.alphabet.index(clip[1])
			sprite.clip.use(cy, cx)
			x, y = pos[0]*GRID, pos[1]*GRID
			# print self.room_x, self.room_y
			x += self.x*GRID; y += self.y*GRID
			sprite.goto = x, y
			return sprite

		x, y = pos[0], pos[1]
		tile = make_tile(pos, clip)
		self.tiles[x][y] = tile
		self.data[x][y] = clip

	def empty_tile(self, pos=(), clip=()):
	#I exist entirely for ERoom's sake.
		return None

	def draw(self):
		# if self.tiles[0][0] != None:
		# 	self.tiles[0][0].draw()
		for x in self.tiles:
			for y in x:
				if y != None:
					y.draw()


#	LOADING DATA

	def _load_room(self, room_dir):
	#Loads and formats the Room for usage.

		def get_data(room_dir):
		#Grab Room data from text file.
			self.name = room_dir
			room_dir = "outside/levels/%s.txt" % room_dir
			
			try: #loading the file...
				f = open(room_dir)
				room = f.read()
				f.close()
			except: #If that fails, use a generic template.
				room = "_template"

			return room

		def grab_texture(data):
		#Load the texture from the first data data line.
			#Grab and remove the texture line.
			self.texture_name = data.split("\n")[0]
			tex_dir = "img/tilemaps/%s.png" \
			% self.texture_name
			self.texture = MyTexture(tex_dir)

			lvl = ""
			for line in data.split("\n")[1:]:
				lvl += str(line) + "\n"

			return lvl[:-1]

		def format_data(data):
		#The data is now in an [x][y] format.
			rows = data.split("\n")
			format = []
			i = 0
			while i < len(rows[0])-1:
				format.append([c[i]+c[i+1] for c in rows])
				i += 2
			return format

		def room_off_data(data):
		#The data should be room-sized.
			def room_w():
				room = ROOM_WIDTH/GRID
				w = room
				while w < len(data)-1:
					w += room
				return w
			def room_h(x):
				room = ROOM_HEIGHT/GRID
				h = room
				while h < len(data[0])-1:
					h += room
				return h
			#
			data_w = lambda: len(data)
			data_h = lambda x: len(data[x])

			#Append pre-existing columns.
			x = 0
			while x < room_w():

				#Add new column if needed.
				if x >= data_w():
					data.append([])

				y = data_h(x)
				while y < room_h(x):
					data[x].append("__")
					y += 1
				y = 0
				x += 1

			return data

		data = get_data(room_dir)
		data = grab_texture(data)
		data = format_data(data)
		data = room_off_data(data)
		return data
		# return [["aa"]]

#	TILE CREATION

	def _initialize_tiles(self, data):
	#Make spaces for the tiles to reside in.
		tiles = []
		fill = [None for y in data[0]]
		while len(tiles) < len(data):
			tiles.append(fill)

		# return tiles
		return [tile[:] for tile in tiles]


	def _make_all_tiles(self, data):
	#Make ALL of the tiles in the data.
		for ix, x in enumerate(data):
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
					and self.data[x][y] != "__":

						self.change_tile((x, y),\
						 self.data[x][y])

				#Remove any tiles outside of the area.
				if x < x1 or x2 < x\
				or y < y1 or y2 < y:

					self.tiles[x][y] = None

# DEBUGGING

	def data_ascii(self, data=None):
	#Return the data in an ASCII-kinda style.
		if data == None: data = self.data
		text = ""
		text += self.texture_name+"\n"
		for iy, y in enumerate(data[0]):
			for ix, x in enumerate(data):
				text += str(data[ix][iy])
			text += "\n"
		text = text[:-1]
		return text

	@property
	def filled_data(self):
	#How many tiles are solid, and not empty.
		amt = 0
		for x in self.data:
			for y in x:
				if y != "__":
					amt += 1
		return amt

	@property
	def tiles_loaded(self):
	#Return all the loaded tiles.
		loaded = []
		for x in self.tiles:
			for y in x:
				if y != None:
					loaded.append(y)
		return loaded

	def say_tiles(self):
	#Say how many tiles are loaded out of the room's
	#potential total.
		total = self.w * self.h
		loaded = len(self.tiles_loaded)

		string = "%s loaded (%s/%s) tiles."\
		% (self.name, loaded, total)
		print string

	def say_textures(self):
	#Say the amount of individual textures being used
	#by the tiles.
		amt = 0
		old = None
		for x in self.tiles:
			for y in x:
				if y.texture != old:
					amt += 1
				old = y.texture



#

class collision:
#Bounds all of the tiles together to handle only a few
#collision points.
	def __init__ (self, Room): self._ = Room

	# TILE COLLISION
	#For reading a %name%_collision.txt to interpret
	#what tiles have what kind of collision.

	def filler(self):
		self.read_collisions()

	def read_collisions(self):
	#Make collision data.

	#READ the data from a file.
		collision_dir = "img/tilemaps/%s_collision.txt"\
		 % self._.texture_name
		try:
			f = open(collision_dir,"r+")
			_raw = f.read()
		except:
			#Make and save as the DEFAULT.
			f = open(collision_dir,"w")
			w = self._.texture.width/GRID
			h = self._.texture.height/GRID
			txt = ""
			for x in range(w):
				if txt != "": txt = txt+"\n"
				for y in range(h):
					txt = txt+"aa"
			f.write(txt)
			_raw = txt

		raw = _raw
		f.close()

		#CONVERT into usable collision data.
		self.tileset = []
		raw = raw.split("\n")
		for line in raw:
			self.tileset.append([])
			c = 0
			while c < len(line):
				self.tileset[-1].append(line[c:c+2])
				c += 2

		# #x/y format
		# xy_tileset = []
		# row = 0
		# while row < len(self.tileset[0]):
		# 	column = [i[row] for i in self.tileset] 
		# 	xy_tileset.append(column[:])
		# 	row += 1
		# self.tileset = [i[:] for i in xy_tileset]

		# #debug
		# if self._.name == "aa":
		# 	print self.tileset

	#USE tileset data to make room DATA.
		self.data = []

		for x in self._.data:
			self.data.append([])
			for y in x:

				#Using the data character, get the
				#position on the collision tileset.
				if y == "__":
					self.data[-1].append("__")
				else:
					c1, c2 = y
					cx = self._.alphabet.index(c1)
					cy = self._.alphabet.index(c2)
					tileset_data = self.tileset[cx][cy]
					self.data[-1].append(tileset_data)

		#x/y format
		# xy_data = []
		# row = 0
		# while row < len(self.data[0]):
		# 	column = [i[row] for i in self.data] 
		# 	xy_data.append(column[:])
		# 	row += 1
		# self.data = [i[:] for i in xy_data]

		# # #debug
		# if self._.name == "aa": 
		# 	print self._.data_ascii(self.data)
		# 	print self._.data_ascii(self._.data)