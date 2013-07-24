from modules.level import Level
from modules.pysfml_game import ROOM_HEIGHT, ROOM_WIDTH
from modules.pysfml_game import GRID
from modules.pysfml_game import MyTexture, MySprite

class ELevel(Level):
#A level-editor specific version of Level.
#Designed to be altered.

# 	SINGLE-IMAGE TEST

	def __init__(self, arg, x, y):
		Level.__init__(self, arg, x, y)

		#Make image.
		texture = MyTexture("img/still.png")
		self.test = MySprite(texture)
		self.test.goto = self.x*GRID, self.y*GRID

	def draw(self):
		Level.draw(self)
		self.test.draw()


#	GRID

	grid_tex = MyTexture("img/level_editor/grid.png")

	def empty_tile(self, pos=()):
	#Forwarded from Level.
		x, y = pos
		return self.make_grid(x, y)


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


	#Copy and Paste from Level
	#Tries to cover up ALL empty tiles.

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
					if x == 0 and y == 0:
						if self.tiles[x][y] == None:
						### Only this line has been removed.

							self.change_tile((x, y),\
							 self.level[x][y])

				#Remove any tiles outside of the area.
				if x < x1 or x2 < x\
				or y < y1 or y2 < y:

					self.tiles[x][y] = None


#	TEXTURE

	def change_texture(self, texture_name):
		self.texture_name = texture_name
		tex_dir = "img/tilemaps/%s.png" % texture_name
		self.texture = MyTexture(tex_dir)

		#Update all of the tiles' textures.
		for x in self.tiles:
			for y in x:
				if y != None:
					y.texture = self.texture

#	SAVING

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