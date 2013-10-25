from code.pysfml_game import MyTexture, MySprite

class tile: #toolbox
# Adds and removes tiles to and fro the WorldMap.
# Selects tiles from a tilemap.
	
	def __init__(self):
		self.tilemap = None
		self.selected = "0000"

	def draw(self):
		if self.tilemap != None: self.tilemap.draw()


	def controls(self, worldmap, mouse, key, cursor):

		if not self.is_open:
			if mouse.left.held():
				self.create(worldmap, cursor)
			if mouse.right.held():
				self.remove(worldmap, cursor)

		if key.L_SHIFT.pressed():
			self.open(worldmap, cursor)
		if key.L_SHIFT.released():
			self.close()

		if self.is_open:
			if mouse.left.pressed():
				self.select(cursor)


	####

	#controls

	def create(self, worldmap, cursor):
		x, y = cursor.tile_position
		if worldmap.in_tile_points((x+1,y+1)):
			worldmap.tiles[x][y].change(self.selected)

	def remove(self, worldmap, cursor):
		x, y = cursor.tile_position
		if worldmap.in_tile_points((x+1,y+1)):
			worldmap.tiles[x][y].change("____")


	#tilemap

	@property
	def is_open(self): return bool(self.tilemap != None)

	def open(self, worldmap, cursor):
		if self.tilemap == None:
			self.tilemap = self._tilemap(worldmap, cursor)

	def close(self):
		if self.tilemap != None:
			self.tilemap = None

	def select(self, cursor):

		#proportional pos from the tilesheet
		x,y = cursor.tile_position
		ox,oy = self.tilemap.sprite.tile_position
		x -= ox; y -= oy

		if x < 0: x = 0
		if x > self.tilemap.sprite.tile_w:
			x = self.tilemap.sprite.tile_w
		if y < 0: y = 0
		if y > self.tilemap.sprite.tile_h:
			y =self.tilemap.sprite.tile_h


		#make key
		x,y = str(x), str(y)
		if len(x) == 1: x = "0"+x
		if len(y) == 1: y = "0"+y

		self.selected = x+y

	##

	class _tilemap:

		def __init__(self, worldmap, cursor):

			#sprite
			x,y = cursor.room_position
			texture = \
			worldmap.rooms[x][y].graphics.texture
			self.sprite = MySprite(texture)

			x,y = cursor.tile_position
			self.sprite.tile_position = x,y

		def draw(self):
			self.sprite.draw()
