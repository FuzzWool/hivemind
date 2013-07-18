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
		if self.render_sprite != None:
			self.render_sprite.x = arg*GRID

	@property
	def y(self): return self._y
	@y.setter
	def y(self, arg):
		self._y = arg
		if self.render_sprite != None:
			self.render_sprite.y = arg*GRID

	@property
	def w(self): return len(self.level)
	@w.setter
	def w(self, arg):
		change = arg - self.w
		if change >= +1: self.expand_right(arg)
		if change <= -1: self.shrink_right(arg)
		self.make_render()

	@property
	def h(self): return len(self.level[0])
	@h.setter
	def h(self, arg):
		change = arg - self.h
		if change >= +1: self.expand_bottom(arg)
		if change <= -1: self.shrink_bottom(arg)
		self.make_render()

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
	@room_w.setter
	def room_w(self, arg): self.w = arg*(ROOM_WIDTH/GRID)

	@property
	def room_h(self): return int(self.h*GRID / ROOM_HEIGHT)
	@room_h.setter
	def room_h(self, arg): self.h = arg*(ROOM_HEIGHT/GRID)
	#

	def __call__(self): return self.level
	
	def __init__ (self, level_dir):
	#Grabs level data and creates tiles.

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

		self.make_render()


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


	#RENDERING
	#For moving the level as a whole.
	render_sprite = None
	render_texture = None

	def make_render(self):
	#Remake the render texture, and then the sprite.
	#For any instances in which the graphics may change.
		render \
		= sf.RenderTexture(self.w*GRID, self.h*GRID)

		for ix, x in enumerate(self.tiles):
			for iy, y in enumerate(x):
				if self.tiles[ix][iy] != None:
					render.draw(self.tiles[ix][iy])
				else:
					try:
						render.draw(self.grid[ix][iy])
					except:
						pass

		self.render_texture = render
		self.render_texture.display()
		self.render_sprite = MySprite(self.render_texture.texture)
		self.render_sprite.goto = self.x*GRID, self.y*GRID

	def draw(self):
		if self.render_sprite != None:
			self.render_sprite.draw()