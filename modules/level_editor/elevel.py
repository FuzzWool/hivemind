from modules.level import Level
from modules.pysfml_game import ROOM_HEIGHT, ROOM_WIDTH
from modules.pysfml_game import GRID
from modules.pysfml_game import MyTexture, MySprite

class ELevel(Level):
#A level-editor specific version of Level.
	grid = []
	grid_tex = MyTexture("img/level_editor/grid.png")

	#How much the level has been pushed.
	offset_x, offset_y = 0, 0


	def __init__ (self, level_dir):
	#Grid is initialized to match the Level's size.
		super(ELevel, self).__init__(level_dir)

		for ix, x in enumerate(self.level):
			if ix >= len(self.grid):
				self.grid.append([])
			
			for iy, y in enumerate(self.level[ix]):
				if iy >= len(self.grid[ix]):
					self.grid[ix].append(None)

				self.grid[ix][iy] = self.make_grid(ix, iy)


	def change_tile(self, pos=(), clip=()):
	#When tiles are changed out-of-bounds, add filler.
		def refresh():
			x, y = pos[0], pos[1]
			x += self.offset_x; y += self.offset_y
			return x, y

		#No going out of bounds.
		x, y = refresh()
		if x < 0 or y < 0: return
		if x > len(self.level)-1: return
		if y > len(self.level[0])-1: return


		x, y = pos[0], pos[1]
		# self.expand_left(x)
		# self.expand_top(y)
		# x, y = refresh()
		# self.expand_bottom(y)
		# self.expand_right(x)

		def make_tile(pos=(), clip=()):
		#Make a new tile. Requires filler to be in place.
			if clip == "__":
				return None
			#
			sprite = MySprite(self.texture)
			sprite.clip.set(GRID, GRID)
			cx = self.alphabet.index(clip[0])
			cy = self.alphabet.index(clip[1])
			sprite.clip.use(cy, cx)
			x = (pos[0] - self.offset_x) * GRID
			y = (pos[1] - self.offset_y) * GRID
			sprite.goto = x, y
			return sprite

		x, y = refresh()
		tile = make_tile((x, y), clip)
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

	def test(self):
		text = ""
		for iy, y in enumerate(self.level[0]):
			for ix, x in enumerate(self.level):
				text += str(self.level[ix][iy])		
			text += "\n"
		text = text[:-1]
		return text

	def draw(self):
		for x in self.grid:
			for y in x:
				if y != None:
					y.draw()
		super(ELevel, self).draw()


#

	#For expanding the level's boundaries.
	def expand_left(self, x):
		offset_x = self.offset_x
		if x < -offset_x:
			
			#Room-sized increments.
			loop_amt = -x + -offset_x
			# room_width = 0
			# while room_width < loop_amt:
			# 	room_width += ROOM_WIDTH / GRID
			# loop_amt = room_width


			for loop in range(loop_amt):
				#Add new columns
				level = self.level
				tiles = self.tiles
				l_fill = ["__" for i in level[0]]
				t_fill = [None for i in level[0]]
				level = [l_fill] + level
				tiles = [t_fill] + tiles
				self.level = [l[:] for l in level]
				self.tiles = [t[:] for t in tiles]

				#Extend the grid's lists
				g_fill = [None for i in level[0]]
				self.grid = [g_fill] + self.grid
				for iy, y in enumerate(self.grid[0]):
					self.grid[0][iy] = \
					self.make_grid(-1, iy)

				#Acknowledge the change
				self.offset_x += 1

	def expand_top(self, y):
		offset_y = self.offset_y
		if y < -offset_y:

			#Room-sized increments.
			loop_amt = -y + -offset_y
			# room_height = 0
			# while room_height < loop_amt:
			# 	room_height += ROOM_HEIGHT / GRID
			# loop_amt = room_height

			for loop in range(loop_amt):
				#Add to columns
				level = self.level
				tiles = self.tiles
				for ic, column in enumerate(level):
					level[ic] = ["__"] + level[ic]
				for it, tile in enumerate(tiles):
					tiles[it] = [None] + tiles[it]
				self.level = [l[:] for l in level]
				self.tiles = [t[:] for t in tiles]

				#Add the new grid tiles to the columns.
				self.grid = \
				[[None] + i[:] for i in self.grid]
				for ix, x in enumerate(self.grid):
					self.grid[ix][0] = \
					 self.make_grid(ix, -1)

				#Acknowledge
				self.offset_y += 1


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

	def expand_bottom(self, y):
	#Add filler tiles to the bottom.

		#Variables
		level_w = lambda: len(self.level)
		level_h = lambda x: len(self.level[x])

		#Processing
		x = 0
		while x < level_w():
			while level_h(x) <= y:
				self.level[x].append("__")
				self.tiles[x].append(None)

				g = self.make_grid(x, level_h(x)-1)
				self.grid[x].append(g)
			x += 1
	#

	def make_grid(self, x, y):
	#Makes a new grid tile.
		grid = MySprite(self.grid_tex)
		grid.clip.set(25, 25)
		grid.clip.use(0, 0)
		grid.x = (x - self.offset_x) * GRID
		grid.y = (y - self.offset_y) * GRID
		return grid