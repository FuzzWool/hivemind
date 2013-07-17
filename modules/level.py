import modules as mo

class Level(object):
	name = ""
	texture_name = ""
	texture = "loaded from the first level file line"
	level = []; tiles = []
	alphabet = ["a","b","c","d","e","f","g",\
	 "h","i","j","k","l","m","n","o","p","q",\
	 "q","r","s","t","u","v","w","x","y","z"]

	def __call__(self): return self.level
	
	def __init__ (self, level_dir):
	#Grabs level data and creates tiles.

		def get_level(level_dir):
		#Grab level data from text file.
			self.name = level_dir
			f = open("outside/levels/"+level_dir+".txt")
			level = f.read()
			f.close()
			return level

		def grab_texture(level):
		#Load the texture from the first level data line.
			#Grab and remove the texture line.
			self.texture_name = level.split("\n")[0]
			self.texture = mo.texture(self.texture_name)

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

		def initialize_tiles(level):
		#Make empty spaces for tiles using the level size.
			tiles = []
			fill = [None for y in level[0]]
			while len(tiles) < len(level):
				tiles.append(fill)
			return tiles

		def make_tiles(level):
		#Add tile graphics based on the level[x][y]
			for ix, x in enumerate(level):
				for iy, y in enumerate(x):
					self.change_tile((ix, iy), y)

		level = get_level(level_dir)
		level = grab_texture(level)
		level = format_level(level)
		level = room_off_level(level)
		self.level = level

		tiles = initialize_tiles(self.level)
		self.tiles = [tile[:] for tile in tiles]

		make_tiles(self.level)


	def change_tile(self, pos, clip):
	#Changes a tile, updates the level and tiles.

		def make_tile(pos=(), clip=()):
		#Make a new tile. Requires filler to be in place.
			if clip == "__":
				return None
			#
			sprite = mo.MySprite(self.texture)
			sprite.clip.set(mo.GRID, mo.GRID)
			cx = self.alphabet.index(clip[0])
			cy = self.alphabet.index(clip[1])
			sprite.clip.use(cy, cx)
			sprite.goto = pos[0]*mo.GRID, pos[1]*mo.GRID
			return sprite

		x, y = pos[0], pos[1]
		tile = make_tile(pos, clip)
		self.tiles[x][y] = tile
		self.level[x][y] = clip
		

	def draw(self):
		# tiles[x][y]
		for x in self.tiles:
			for y in x:
				if y != None:
					y.draw()