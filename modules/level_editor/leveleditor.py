import modules as mo

class LevelEditor:
#Alters the data of the currently loaded level.

	#External classes.
	Mouse = None
	Camera = None
	Level = None

	#Sprites
	mouse_tex = mo.texture("img/level_editor/cursor.png")
	mouse = mo.MySprite(mouse_tex)

	def __init__(self, Mouse, Camera, Level):
		self.Mouse = Mouse
		self.Camera = Camera
		self.Level = Level

		#Subclasses
		self.TileSelector = TileSelector(self)

	def place_tile(self, tile_data=None):
	#Changes a tile within the level.
	#Level, Mouse, TileSelector
		x, y = self.Mouse.grid_position(self.Camera)
		if self.TileSelector.visible == False:
			if tile_data == None:
				tile_data = self.TileSelector.select_tile
			self.Level.change_tile((x, y), tile_data)

	def remove_tile(self):
		self.place_tile("__")

	def draw(self):
		self._move_cursor()

		#draw Grid externally
		self.TileSelector.draw()
		self.mouse.draw()

	#

	def _move_cursor(self):
		x, y = self.Mouse.grid_position(self.Camera)
		x *= mo.GRID; y *= mo.GRID
		self.mouse.goto = x, y


class TileSelector:
#A pop-up for selecting tiles in the Level Editor.
	
	#Logic
	visible = False
	select_tile = "aa"

	#Graphics
	b_sprite = None; tiles = []
	cursor = None

	def __init__ (self, LevelEditor):
		self._ = LevelEditor

		def make_box(texture, w, h):
			b_sprite = mo.MySprite(texture)
			b_sprite.clip.set(25, 25)
			b_sprite.goto = 500, 200

			b_sprite.box.size = w, h
			b_sprite.box.center = b_sprite.center
			self.b_sprite = b_sprite

		def make_tiles(texture, w, h):
			literal_w, literal_h = w, h
			grid_w = literal_w/mo.GRID
			grid_h = literal_h/mo.GRID

			#They are binded as children to the box.
			for x in range(grid_w):
				self.tiles.append([])
				for y in range(grid_h):
					tile = mo.MySprite(texture)
					tile.clip.set(25, 25)
					tile.clip.use(x, y)
					tile.goto = self.b_sprite.box.goto
					tile.move(x*mo.GRID, y*mo.GRID)
					self.b_sprite.children.append(tile)
					self.tiles[-1].append(tile)

		def make_cursor():
			tex = self._.mouse_tex
			cursor = mo.MySprite(tex)
			cursor.clip.set(25, 25)
			cursor.goto = self.tiles[0][0].goto
			self.cursor = cursor
			self.b_sprite.children.append(self.cursor)

		texture = self._.Level.texture
		w, h = 300, 300
		make_box(texture, w, h)
		make_tiles(texture, w, h)
		make_cursor()


	def toggle(self, visible=None):
	#Opens/closes the TileSelector.
		if visible == None: visible = not self.visible
		self.visible = visible
		#Moves the tiles.
		x, y = self._.Mouse.grid_position(self._.Camera)
		x *= mo.GRID; y *= mo.GRID
		self.b_sprite.box.center = x, y
		self.b_sprite.center = x, y

	def open(self): self.toggle(True)
	def close(self): self.toggle(False)


	def select(self):
	#Select a tile. Change selected tile, move the cursor.
		if self.visible:

			def grid_relative():
				x, y = self._.Mouse.grid_position\
					(self._.Camera)
				x -= self.tiles[0][0].x/mo.GRID
				y -= self.tiles[0][0].y/mo.GRID
				return x, y

			def in_bounds(x, y):
				bound_w = self.b_sprite.box.w/mo.GRID-1
				bound_h = self.b_sprite.box.h/mo.GRID-1

				if 0 > x or x > bound_w\
				or 0 > y or y > bound_h:
					return False
				return True

			def change_select(x, y):
				a = self._.Level.alphabet[int(y)]
				b = self._.Level.alphabet[int(x)]
				self.select_tile = a+b
				
			def move_cursor(x, y):
				self.cursor.goto = self.tiles[0][0].goto
				x *= mo.GRID; y *= mo.GRID
				self.cursor.move(x, y)
			
			x, y = grid_relative()
			if not in_bounds(x, y):
				return
			change_select(x, y)
			move_cursor(x, y)


	def draw(self):
		#Box and Tiles
		if self.visible == True:
			self.b_sprite.box.draw()
			for x in self.tiles:
				for y in x:
					y.draw()
			#Cursor
			self.cursor.draw()