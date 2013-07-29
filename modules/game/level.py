from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import GRID
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

		self.collision = collision(self)


	def change_tile(self, pos, clip):
	#Changes a tile, updates the level and tiles.

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
			self.texture = MyTexture(tex_dir)

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
				room = ROOM_WIDTH/GRID
				w = room
				while w < len(level)-1:
					w += room
				return w
			def room_h(x):
				room = ROOM_HEIGHT/GRID
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

	def level_ascii(self, level=None):
	#Return the level in an ASCII-kinda style.
		if level == None: level = self.level
		text = ""
		text += self.texture_name+"\n"
		for iy, y in enumerate(level[0]):
			for ix, x in enumerate(level):
				text += str(level[ix][iy])
			text += "\n"
		text = text[:-1]
		return text

	@property
	def filled_level(self):
	#How many tiles are solid, and not empty.
		amt = 0
		for x in self.level:
			for y in x:
				if y != "__":
					amt += 1
		return amt

	@property
	def tiles_loaded(self):
	#Retrun all the loaded tiles.
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

#

class collision:
#Bounds all of the tiles together to handle only a few
#collision points.

	@property
	def points(self):
	#Return all of the room's collision points.
	#Returns absolute values
		points = []
		old = []
		for x in self._bounds:
			for y in x:
				if y not in old and y != None:
					old.append(y)
					x1, y1 = (y.x1)*GRID, (y.y1)*GRID
					x2, y2 = (y.x2+1)*GRID, (y.y2+1)*GRID

					#offset
					ox = self._.x*GRID
					oy = self._.y*GRID
					x1, y1 = x1 + ox, y1 + oy
					x2, y2 = x2 + ox, y2 + oy

					point = (x1, y1, x2, y2)
					points.append(point)
		return points


	###WIP
	def points_range(self, rx1, ry1, rx2, ry2):
	#Returns all of the room's collision points.
	#...within a certain grid range.

		#Positioning offset
		rx1 -= self._.x; rx2 -= self._.x
		ry1 -= self._.y; ry2 -= self._.y
		if rx1 < 1: rx1 = 0
		if ry1 < 1: ry1 = 0

		points = []
		old = []

		for x in self._bounds[rx1:rx2]:
			for y in x[ry1:ry2]:

				if y not in old and y != None:
					old.append(y)
					x1, y1 = (y.x1)*GRID, (y.y1)*GRID
					x2, y2 = (y.x2+1)*GRID, (y.y2+1)*GRID

					#offset
					ox = self._.x*GRID
					oy = self._.y*GRID
					x1, y1 = x1 + ox, y1 + oy
					x2, y2 = x2 + ox, y2 + oy

					point = (x1, y1, x2, y2)
					points.append(point)
		return points
	###

	#

	def __init__ (self, Level):
		self._ = Level
		self._create_bounds()

	class bound:
	#Coordinates to be referenced in multiple tiles.
		x1, y1, x2, y2 = None, None, None, None

		@property
		def points(self):
			return self.x1, self.y1, self.x2, self.y2


	def _create_bounds(self):	
		#Create bounding boxes.
		
		#Grid format.
		#Every space which is filled has a bound.
		#The bound is a reference to the original x1, y1.

		self._bounds = []
		#Every column has a bound.
		for ix, x in enumerate(self._.level):
			self._bounds.append([])

			old = None
			for iy, y in enumerate(x):

				#If there's a tile...
				if y != "__":
					#And there wasn't a tile beforehand.
					if old == "__"\
					or iy == 0:
						#Make a new bound.
						bound = self.bound()
						bound.x1, bound.x2 = ix, ix
						bound.y1, bound.y2 = iy, iy
						self._bounds[-1].append(bound)

					#And there WAS a tile beforehand.
					else:
						#Use that bound.
						bound = self._bounds[-1][-1]
						bound.x2, bound.y2 = ix, iy
						self._bounds[-1].append(bound)

				#If there isn't a tile.
				else:
					#Add an empty space.
					self._bounds[-1].append(None)

				old = y

		# #Merge the columns together.
		w = len(self._bounds)
		h = len(self._bounds[0])

		for x in range(1, w):
			for y in range(h):

				#If they're aligned, merge them.
				a = self._bounds[x-1][y]
				b = self._bounds[x][y]
				if a != None and b != None:
					if (a.y1,a.y2) == (b.y1,b.y2):
						#Expand a.
						a.x2 = b.x2

						#Convert b to a.
						for y2 in range(h):
							if self._bounds[x][y2] == b:
								self._bounds[x][y2] = a
						b = a
						# print x, y, b

		# self.say_bounds()


	#Debugging
	def say_bounds(self):
		unique = 0
		old = []
		for x in self._bounds:
			for y in x:
				if y not in old and y != None:
					print y.points
					unique += 1
				old.append(y)

		msg = "Using %s bounds from %s tiles."\
		% (unique, self._.filled_level)
		print msg