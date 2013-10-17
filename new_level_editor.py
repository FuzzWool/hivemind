from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

from code.game import WorldMap
worldmap = WorldMap(4,4)


###########
from code.pysfml_game import MyTexture, MySprite

class toolbox:
	
	def __init__(self):
		self._init_cursor()
		self.tile = tile()

	def draw(self, mouse):
		self.tile.draw()
		self._draw_cursor(mouse)

	def controls(self, worldmap, mouse, key):
		self.tile.controls(worldmap, mouse, key)

		if key.L_CTRL.held():
			if key.S.pressed():
				worldmap.save()
	#



	#cursor
	def _init_cursor(self): #init
		cursor_tex \
		= MyTexture("assets/level_editor/cursor.png")
		self.cursor = MySprite(cursor_tex)

	def _draw_cursor(self, mouse): #draw
		self.cursor.tile_position = mouse.tile_position
		self.cursor.draw()
	#


class tile:
# Adds and removes tiles to and fro the WorldMap.
# Selects tiles from a tilemap.
	
	def __init__(self):
		self.tilemap = None
		self.selected = "0000"

	def draw(self):
		if self.tilemap != None: self.tilemap.draw()


	def controls(self, worldmap, mouse, key):

		if not self.is_open:
			if mouse.left.held():
				self.create(worldmap, mouse)
			if mouse.right.held():
				self.remove(worldmap, mouse)

		if key.L_SHIFT.pressed():
			self.open(worldmap, mouse)
		if key.L_SHIFT.released():
			self.close()

		if self.is_open:
			if mouse.left.pressed():
				self.select(mouse)


	####

	#controls

	def create(self, worldmap, mouse):
		x, y = mouse.tile_position
		worldmap.tiles[x][y].change(self.selected)

	def remove(self, worldmap, mouse):
		x, y = mouse.tile_position
		worldmap.tiles[x][y].change("____")


	#tilemap

	@property
	def is_open(self): return bool(self.tilemap != None)

	def open(self, worldmap, mouse):
		if self.tilemap == None:
			self.tilemap = self._tilemap(worldmap, mouse)

	def close(self):
		if self.tilemap != None:
			self.tilemap = None

	def select(self, mouse):

		#proportional pos from the tilesheet
		x,y = mouse.tile_position
		ox,oy = self.tilemap.sprite.tile_position
		x -= ox; y -= oy
		x,y = self.tilemap.sprite.keep_in_tile_size(x,y)

		#make key
		x,y = str(x), str(y)
		if len(x) == 1: x = "0"+x
		if len(y) == 1: y = "0"+x

		self.selected = x+y

	##

	class _tilemap:

		def __init__(self, worldmap, mouse):

			#sprite
			x,y = mouse.room_position
			texture = worldmap.rooms[x][y].texture
			self.sprite = MySprite(texture)

			x,y = mouse.tile_position
			self.sprite.tile_position = x,y

		def draw(self):
			self.sprite.draw()

	##


#########################################################
from code.pysfml_game import MyMouse

mouse = MyMouse()
TB = toolbox() ###


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	TB.controls(worldmap, mouse, key) ###

	key.reset_all()

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()

	TB.draw(mouse) ###

	#
	window.display()