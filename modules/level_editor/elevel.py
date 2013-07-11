from modules.level import Level
from modules.pysfml_game import ROOM_HEIGHT, ROOM_WIDTH
from modules.pysfml_game import GRID
from modules.pysfml_game import MyTexture, MySprite

class ELevel(Level):
#A level-editor specific version of Level.
	grid = []
	grid_tex = MyTexture("img/level_editor/grid.png")

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
				grid.x = x * GRID
				grid.y = y * GRID
				self.grid[x][y] = grid

			select_x += 1; select_y += 1

			level_x = len(self.level)
			level_y = lambda x: len(self.level[x])

			if select_x < level_x:
				select_x = level_x
			if select_y < level_y(0):
				select_y = level_y(0)

			#Change to being an x/y loop.
			x = 0 #Go through the whole level.
			while x < select_x:
				
				if x >= level_x:
					self.level.append([])
					self.tiles.append([])
					self.grid.append([])##

				y = level_y(x) #Go only to column changes.
				while y < select_y:
					self.level[x].append("__")
					self.tiles[x].append(None)

					self.grid[x].append(None)##
					new_grid(x, y)
					
					y += 1

				x += 1

		x, y = pos[0], pos[1]
		add_filler(x, y)
		super(ELevel, self).change_tile(pos, clip)


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
		for x in self.grid:
			for y in x:
				if y != None:
					y.draw()
		super(ELevel, self).draw()