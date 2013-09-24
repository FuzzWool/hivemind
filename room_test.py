#Make a new ROOM class from scratch.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0,0


#####
from modules.pysfml_game import\
 RENDER_WIDTH, RENDER_HEIGHT
from modules.pysfml_game import GRID

class Room(object):

	# SPRITE HANDLING

	def __init__(self, x=0, y=0):
		self.texture = MyTexture("img/tilemaps/level.png")
		self.x, self.y = x, y
		self.tiles = self.load(self.x, self.y)

	def load(self, room_x=0, room_y=0):
		#LOAD and POSITION the tiles.
		#Consider the ROOM OFFSET.

		tiles = []
		w, h = RENDER_WIDTH/GRID, RENDER_HEIGHT/GRID
		room_x *= RENDER_WIDTH/GRID
		room_y *= RENDER_HEIGHT/GRID

		for x in range(w):
			tiles.append([])
			for y in range(h):
				tile = self.Tile()
				tile.load(self.texture)
				tile.x, tile.y = room_x+x, room_y+y
				tiles[-1].append(tile)
		return tiles

	def draw(self):
		for x in self.tiles:
			for y in x:
				y.draw()



	class Tile(object):

		def __init__(self):
			self.sprite = None

		# SPRITE HANDLING

		def load(self, texture):
			self.sprite = MySprite(texture)
			self.sprite.clip.set(GRID,GRID)

		def draw(self):
			self.sprite.draw()

		# POSITION

		@property
		def x(self): return self.sprite.x/GRID
		@x.setter
		def x(self, x): self.sprite.x = x*GRID
		#
		@property
		def y(self): return self.sprite.y/GRID
		@y.setter
		def y(self, y): self.sprite.y = y*GRID


####

class WorldMap:
#Loads MULTIPLE ROOMS.
#Provides shorthands for accessing all the rooms as one.
	
	def __init__(self):
	#Load all of the ROOMS.
		self.rooms = self.load(2,2)


	# TILE DRAWING

	def load(self, w=0, h=0):
	#Specify the AMOUNT of rooms to be loaded.
		rooms = []
		for x in range(w):
			rooms.append([])
			for y in range(h):
				room = Room(x,y)
				rooms[-1].append(room)
		return rooms

	def draw(self, camera=None):
	#Draws all of the ROOMS in the game.
	#! Draw only ROOMS shown by a Camera.

		for x in self.rooms:
			for y in x:
				y.draw()



	# TILE ACCESS

	@property
	def tiles(self):
	#An xy-list of the tiles of every single room.
		
		tiles = []
		#Grab every ROOM in a COLUMN.
		for room_x in self.rooms:

			#For every TILE COLUMN...
			tile_w = len(room_x[0].tiles)
			for tile_x in range(tile_w):
				#...grab it from all the ROOMS,
				# and connect them.
				column = []
				for room_y in room_x:
					column += room_y.tiles[tile_x]
				tiles.append(column)

		return tiles

	@property
	def tiles_w(self): return len(self.tiles)
	@property
	def tiles_h(self): return len(self.tiles[0])

####


worldmap = WorldMap()


#########################################################

running = True
while running:
	
	#LOGIC
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	amt = 5
	if key.LEFT.held(): Camera.x -= amt
	if key.RIGHT.held(): Camera.x += amt
	if key.UP.held(): Camera.y -= amt
	if key.DOWN.held(): Camera.y += amt

	#VIDEO
	window.clear(sf.Color.WHITE)
	window.view = Camera
	

	#
	worldmap.draw(10)
	#


	window.display()