import modules as mo
import modules.level_editor as le

ctrl = mo.KeyTracker(mo.sf.Keyboard.L_CONTROL)
s = mo.KeyTracker(mo.sf.Keyboard.S)
mouse = le.EditMouse()

#####
#WIP
class LevelEditor:
	Level = None

	mouse_tex = mo.texture("img/level_editor/cursor.png")
	mouse = mo.MySprite(mouse_tex)

	def __init__(self, Level):
		self.Level = Level
		self.TileSelector = TileSelector(self)

	def move_cursor(self, x, y):
		x *= mo.GRID; y *= mo.GRID
		self.mouse.goto = x, y

	def place_tile(self, x, y, tile_data=None):
	#Changes a tile within the level.
		if self.TileSelector.visible == False:
			if tile_data == None:
				tile_data = self.TileSelector.select_tile
			self.Level.change_tile((x, y), tile_data)

	def remove_tile(self, x, y):
		self.place_tile(x, y, "  ")

	def draw(self):
		self.TileSelector.draw()
		self.mouse.draw()


class TileSelector:
#A pop-up for selecting tiles in the Level Editor.
	
	#Logic
	visible = False
	select_tile = "ab"

	#Graphics
	tiles = []
	b_sprite = None
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
		#Populate the box with all of the other tiles.
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
		#The cursor which highlights the tile in use.
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

	def toggle(self, x, y):
	#Opens/closes the TileSelector.
		self.visible = not self.visible
		#Moves the tiles.
		x *= mo.GRID; y *= mo.GRID
		self.b_sprite.box.center = x, y
		self.b_sprite.center = x, y

	def select(self, gmouse_x, gmouse_y):
	#Select a tile. Change selected tile, move the cursor.
		if self.visible:
			#Change selected tile.
			x, y = gmouse_x, gmouse_y
			x -= self.tiles[0][0].x/mo.GRID
			y -= self.tiles[0][0].y/mo.GRID
			a = self._.Level.alphabet[int(y)]
			b = self._.Level.alphabet[int(x)]
			self.select_tile = a+b
			#Change cursor position.
			self.cursor.goto = self.tiles[0][0].goto
			x *= mo.GRID; y *= mo.GRID
			self.cursor.move(x, y)
			#Close window.
			self.visible = False

	def draw(self):
		#Box and Tiles
		if self.visible == True:
			self.b_sprite.box.draw()
			for x in self.tiles:
				for y in x:
					y.draw()
			#Cursor
			self.cursor.draw()
####


Level = mo.Level("full")
grid = le.make_grid()
LevelEditor = LevelEditor(Level)
#########################################################
running = True
while running:

	#Logic
	if mo.quit(): running = False

	if ctrl.held():

		if s.pressed():
			Level.save()
		if mouse.left.pressed():
		#WIP
			LevelEditor.TileSelector.toggle\
			 (*mouse.grid_position())
		if mouse.right.pressed():
			print LevelEditor.TileSelector.select_tile
	else:
		if mouse.left.held():
			LevelEditor.place_tile(*mouse.grid_position())
		if mouse.right.held():
			LevelEditor.remove_tile(*mouse.grid_position())

		if mouse.left.pressed():
			LevelEditor.TileSelector.select(*mouse.grid_position())

	LevelEditor.move_cursor(*mouse.grid_position())

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#
	for g in grid:
		g.draw()
	Level.draw()
	LevelEditor.draw()
	#
	mo.window.display()