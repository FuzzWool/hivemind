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

		def new_grid(x, y):
			grid = MySprite(self.grid_tex)
			grid.clip.set(25, 25)
			grid.clip.use(0, 0)
			grid.x = x * GRID
			grid.y = y * GRID
			self.grid[x][y] = grid

		for ix, x in enumerate(self.level):
			if ix >= len(self.grid):
				self.grid.append([])
			
			for iy, y in enumerate(self.level[ix]):
				if iy >= len(self.grid[ix]):
					self.grid[ix].append(None)

				new_grid(ix, iy)

	
	def change_tile(self, pos=(), clip=()):
	#When tiles are changed out-of-bounds, add filler.

		def add_filler(select_x, select_y):
		#Adds extra empty spaces in levels and tiles.
		#So that new data may be added.

			def new_grid(x, y):
				grid = MySprite(self.grid_tex)
				grid.clip.set(25, 25)
				grid.clip.use(0, 0)
				grid.x = (x - self.offset_x) * GRID
				grid.y = (y - self.offset_y) * GRID
				self.grid[x][y] = grid

			select_x += 1 + self.offset_x
			select_y += 1 + self.offset_y

			level_x = len(self.level)
			level_y = lambda x: len(self.level[x])

			#If the selection is smaller than the level..
			#Check the whole level, regardless.
			if select_x < level_x:
				select_x = level_x
			if select_y < level_y(0):
				select_y = level_y(0)

			#Size should be room-sized increments.
			room_width = 0
			while room_width < select_x:
				room_width += ROOM_WIDTH / GRID
			select_x = room_width

			room_height = 0
			while room_height < select_y:
				room_height += ROOM_HEIGHT / GRID
			select_y = room_height


			#Change to being an x/y loop.
			x = 0 #Go through the whole level.
			while x < select_x:

				if x >= level_x:
					self.level.append([])
					self.tiles.append([])
					self.grid.append([])##

				y = 0 #Go only to column changes.
				while y < select_y:

					#Check only additions for the column.
					if y >= level_y(x):
						self.level[x].append("__")
						self.tiles[x].append(None)
						self.grid[x].append(None)##
						new_grid(x, y)

					#Check any changes to update the grid
					if len(self.grid) != 0:
						if self.grid[x][y] == None:
							new_grid(x, y)

					y += 1
				x += 1

		x, y = pos[0], pos[1]
		add_filler(x, y)
		x += self.offset_x; y += self.offset_y

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

	def draw(self):
		for x in self.grid:
			for y in x:
				if y != None:
					y.draw()
		super(ELevel, self).draw()