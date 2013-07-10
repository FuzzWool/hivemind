import modules as mo

class Level:
	level = []
	tiles = []
	level_dir = ""
	alphabet = ["a","b","c","d","e","f","g",\
	 "h","i","j","k","l","m","n","o","p","q",\
	 "q","r","s","t","u","v","w","x","y","z"]
	texture = mo.texture("img/test/level.png") 

	def __call__(self): return self.level
	
	def __init__ (self, level_dir):
	#Grabs level data and creates tiles.

		def get_level(level_dir):
		#Grab level data from text file.
			self.level_dir = level_dir
			f = open("outside/levels/"+level_dir+".txt")
			level = f.read()
			f.close()
			return level

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
				while w < len(level):
					w += room
				return w
			def room_h(x):
				room = mo.ROOM_HEIGHT/mo.GRID
				h = room
				while h < len(level[x]):
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
		level = format_level(level)
		level = room_off_level(level)
		self.level = level

		tiles = initialize_tiles(self.level)
		self.tiles = [tile[:] for tile in tiles]

		make_tiles(self.level)


	def change_tile(self, pos, clip):
	#Changes a tile, updates the level and tiles.

		def add_filler(x, y):
		#Adds extra empty spaces in levels and tiles.
		#So that new data may be added.

			def check_whole_level(x, y):
				if x < len(self.level):
					x = len(self.level)
				if y < len(self.level[0]):
					y = len(self.level[0])
				return x, y

			#Boundary to extend to
			x += 1; y += 1
			x, y = check_whole_level(x, y)

			room_h = mo.ROOM_HEIGHT / mo.GRID
			room_w = mo.ROOM_WIDTH / mo.GRID

			#Make the existing columns longer. y
			for ic, column in enumerate(self.level):
				while len(column) < y:
				#Any time the level needs extending...
					for repeat in range(room_h):
						self.level[ic].append("__")
						self.tiles[ic].append(None)

			#Then add more rows. x
			l_filler = ["__" for i in range(y)]
			t_filler = [None for i in range(y)]
			while len(self.level) < x:
				for repeat in range(room_w):
					self.level.append(l_filler[:])
					self.tiles.append(t_filler[:])

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
		add_filler(x, y)

		tile = make_tile(pos, clip)

		self.tiles[x][y] = tile
		self.level[x][y] = clip

	def save(self):
	#Saves the level back in to the file it originated.
		#Grab the data.
		text = ""
		for iy, y in enumerate(self.level[0]):
			for ix, x in enumerate(self.level):
				text += str(self.level[ix][iy])		
			text += "\n"
		text = text[:-1]

		#Save it to the original file.
		f = open("outside/levels/"+self.level_dir+".txt", "r+")
		f.write(text)
		f.close()

		print "Saved level '%s'!" % self.level_dir
		

	def draw(self):
		# tiles[x][y]
		for x in self.tiles:
			for y in x:
				if y != None:
					y.draw()