from modules.level import Level
from modules.pysfml_game import ROOM_HEIGHT, ROOM_WIDTH
from modules.pysfml_game import GRID
from modules.pysfml_game import MyTexture, MySprite
from modules.pysfml_game import sf

class ELevel(Level):
#A level-editor specific version of Level.
#Designed to be altered.

	grid = []
	grid_tex = MyTexture("img/level_editor/grid.png")


	def __init__ (self, level_dir, room_x, room_y):
		self.load_file(level_dir, room_x, room_y)

	def load_file(self, level_dir, room_x, room_y):
		
		#Load the new level.
		super(ELevel, self)\
		.__init__(level_dir, room_x, room_y)

		#Flush any residue.
		# self.room_x, self.room_y = room_x, room_y
		self.grid = []
		self.render_sprite = None
		self.render_texture = None


		#Grid is initialized to match the Level's size.
		for ix, x in enumerate(self.level):
			if ix >= len(self.grid):
				self.grid.append([])
			
			for iy, y in enumerate(self.level[ix]):
				if iy >= len(self.grid[ix]):
					self.grid[ix].append(None)

				self.grid[ix][iy] = self.make_grid(ix, iy)

		#Level is rendered.
		# self.make_render()


	# def change_tile(self, pos=(), clip=()):
	# 	Level.change_tile(self, pos, clip)


	def save(self):
	#Saves the level back in to the file it originated.
		#Grab the data.
		text = ""
		text += self.texture_name+"\n"
		for iy, y in enumerate(self.level[0]):
			for ix, x in enumerate(self.level):
				text += str(self.level[ix][iy])		
			text += "\n"
		text = text[:-1]

		#Save it to the original file.
		#If it has been renamed, make a new file.
		file_dir = "outside/levels/%s.txt" % self.name
		try:
			f = open(file_dir,"r+")
		except:
			f = open(file_dir,"w")
		f.write(text)
		f.close()

		print "Saved level '%s'!" % self.name

#

	def expand_right(self, x):
	#Add filler tiles to the right.
		#Add new level, tiles and grid slots.

		#Variables
		level_w = lambda: len(self.level)

		l_column = ["__" for i in self.level[0]]
		t_column = [None for i in self.level[0]]
		g_column = [None for i in self.level[0]]

		#Processing
		expand_to = x+1
		if expand_to < level_w(): expand_to = level_w()
		
		x = level_w()
		while x < expand_to:

			self.level.append(l_column[:])
			self.tiles.append(t_column[:])
			self.grid.append(g_column[:])

			for iy, y in enumerate(self.grid[0]):
				g = self.make_grid(x, iy)
				self.grid[x][iy] = g

			x += 1

	def shrink_right(self, arg):
	#Remove tiles from the right.
		while arg < self.w:
			del self.level[-1]
			del self.tiles[-1]
			del self.grid[-1]

	def expand_bottom(self, y):
	#Add filler tiles to the bottom.

		#Variables
		level_w = lambda: len(self.level)
		level_h = lambda x: len(self.level[x])

		#Processing
		x = 0
		while x < level_w():
			while level_h(x) < y:
				self.level[x].append("__")
				self.tiles[x].append(None)

				g = self.make_grid(x, level_h(x)-1)
				self.grid[x].append(g)
			x += 1

	def shrink_bottom(self, arg):
		while arg < self.h:
			for ix, x in enumerate(self.level):
				del self.level[ix][-1]
				del self.tiles[ix][-1]
				del self.grid[ix][-1]


#

	def make_grid(self, x, y):
	#Makes a new grid tile.
		grid = MySprite(self.grid_tex)
		grid.clip.set(25, 25)
		if not x % (ROOM_WIDTH/GRID)\
		and not y % (ROOM_HEIGHT/GRID):
			grid.clip.use(1, 0)
		else:
			grid.clip.use(0, 0)
		grid.x = (x + self.x) * GRID
		grid.y = (y + self.y) * GRID
		return grid

#

	def change_texture(self, texture_name):
		self.texture_name = texture_name
		tex_dir = "img/tilemaps/%s.png" % texture_name
		self.texture = MyTexture(tex_dir)

		#Update all of the tiles' textures.
		for x in self.tiles:
			for y in x:
				if y != None:
					y.texture = self.texture

		#Re-render.
		# self.make_render()

#
	def draw(self):
		for x in self.grid:
			for y in x:
				if y != None:
					y.draw()
		Level.draw(self)