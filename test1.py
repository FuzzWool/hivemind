import modules as mo
rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)

class Level:
	tiles = []
	def __init__ (self):

		def get_level():
		#Grab level data from text file.
			f = open("outside/level.txt")
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

		def make_tile(x, y):
		#Make a tile in a specific position.
			tex = mo.sf.Texture.load_from_file\
				("img/test/level.png")
			sprite = mo.MySprite(tex)
			sprite.clip.set(mo.GRID, mo.GRID)
			sprite.clip.use(x, y)
			return sprite

		def make_tiles(level):
		#Add tile graphics based on the level[x][y]
			#Make the tiles.
			alphabet = ["a", "b", "c", "d", "e", "f", "g",\
			"h", "i", "j", "k", "l", "m", "n", "o", "p", "q",\
			"r", "s", "t", "u", "v", "w", "x", "y", "z"]
			for x_i, x in enumerate(level):
				for y_i, y in enumerate(x):
					tile_x = alphabet.index(y[0])
					tile_y = alphabet.index(y[1])
					tile = make_tile(tile_x, tile_y)
					tile.goto = mo.GRID*x_i, mo.GRID*y_i
					tile.move(x_i*10, y_i)
					self.tiles.append(tile)

		level = get_level()
		level = format_level(level)
		make_tiles(level)

	def draw(self):
		for s in self.tiles:
			s.draw()


Level = Level()
#########################################################
running = True
while running:
	
	#Logic
	if mo.quit(): running = False
	if rtrn.pressed():
		pass

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#
	Level.draw()
	#
	mo.window.display()