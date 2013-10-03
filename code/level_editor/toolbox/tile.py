#LevelEditor > ToolBox > Tile tool
from code.pysfml_game import MySprite
from code.pysfml_game import GRID

class Tile:
#A tool for changing and removing tiles.

	def __init__(self, cursor_tex):
		self.Selector = _Selector(cursor_tex)

	def place(self, Level, grid_pos, tile_data=None):
	#Changes a tile within the level.
		x, y = grid_pos
		if self.Selector.visible == False:
			if tile_data == None:
				tile_data = self.Selector.selected_tile

			x -= Level.tile_x; y -= Level.tile_y
			Level.change_tile((x, y), tile_data)

	def remove(self, Level, grid_pos):
		self.place(Level, grid_pos, "____")

	def draw(self):
		self.Selector.draw()


class _Selector:
#A pop-up menu for selecting new tiles.
	
	#Logic
	visible = False
	selected_tile = "0000"

	#Graphics
	b_sprite = None; tiles = []
	cursor = None; cursor_tex = None

	def __init__(self, cursor_tex):
	#Steal the cursor texture.
		self.cursor_tex = cursor_tex

	
	def open(self, Level, grid_pos):
	#Open the menu, redraw all the tiles.
		self._create_graphics(Level)
		
		#Move the tiles.
		x, y = grid_pos
		x *= GRID; y *= GRID
		self.b_sprite.box.center = x, y
		self.b_sprite.center = x, y

		self.visible = True

	def close(self):
	#Close the menu.
		self.visible = False


	def select(self, Level, grid_pos):
	#Select a tile. Change selected tile, move the cursor.
		if self.visible:

			def grid_relative(grid_pos):
				x, y = grid_pos
				x -= self.tiles[0][0].x/GRID
				y -= self.tiles[0][0].y/GRID
				return x, y

			def in_bounds(x, y):
				bound_w = self.b_sprite.box.w/GRID-1
				bound_h = self.b_sprite.box.h/GRID-1

				if 0 > x or x > bound_w\
				or 0 > y or y > bound_h:
					return False
				return True

			def change_select(Level, x, y):
				a = str(int(x))
				b = str(int(y))
				if len(a) == 1: a = "0"+a
				if len(b) == 1: b = "0"+b
				self.selected_tile = a+b
				
			def move_cursor(x, y):
				self.cursor.goto = self.tiles[0][0].goto
				x *= GRID; y *= GRID
				self.cursor.move(x, y)
			
			x, y = grid_relative(grid_pos)
			if not in_bounds(x, y): return
			change_select(Level, x, y)
			move_cursor(x, y)


	def draw(self):
		if self.visible == True:
			self.b_sprite.box.draw()
			for x in self.tiles:
				for y in x:
					y.draw()
			self.cursor.draw()

	#

	def _create_graphics(self, Level):
	#Create the box, tiles and cursor.

		self.b_sprite = None
		self.tiles = []
		self.cursor = None

		def make_box(texture, w, h):
			b_sprite = MySprite(texture)
			b_sprite.clip.set(25, 25)
			b_sprite.goto = 500, 200

			b_sprite.box.size = w, h
			b_sprite.box.center = b_sprite.center
			self.b_sprite = b_sprite

		def make_tiles(texture, w, h):
			literal_w, literal_h = w, h
			grid_w = literal_w/GRID
			grid_h = literal_h/GRID

			#They are binded as children to the box.
			for x in range(grid_w):
				self.tiles.append([])
				for y in range(grid_h):
					tile = MySprite(texture)
					tile.clip.set(25, 25)
					tile.clip.use(x, y)
					tile.goto = self.b_sprite.box.goto
					tile.move(x*GRID, y*GRID)
					self.b_sprite.children.append(tile)
					self.tiles[-1].append(tile)

		def make_cursor():
			tex = self.cursor_tex
			cursor = MySprite(tex)
			cursor.clip.set(25, 25)
			cursor.goto = self.tiles[0][0].goto
			self.cursor = cursor
			self.b_sprite.children.append(self.cursor)

		texture = Level.texture
		w, h = 300, 300
		make_box(texture, w, h)
		make_tiles(texture, w, h)
		make_cursor()