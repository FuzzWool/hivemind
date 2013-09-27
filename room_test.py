#Make a new ROOM class from scratch.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0,0

#####

from modules.pysfml_game import\
 RENDER_WIDTH, RENDER_HEIGHT
from modules.pysfml_game import GRID

# STATIC - Load ALL of the textures in advance.
textures = {}

import glob
import os
directory = "img/tilemaps"
os.chdir(directory)
for filename in glob.glob("*.png"):
	texture = MyTexture(filename)
	textures[filename] = texture
os.chdir("../../")
# 

class Room(object):


	# SPRITE HANDLING

	def __init__(self, x=0, y=0, texture="level.png",\
		load_immediately=True):
		#Grab the Room's POSITION.
		#Grab the TEXTURE for all the sprites.

		#TEST
		if (x % 2 == 0 and y % 2 != 0)\
		or (x % 2 != 0 and y % 2 == 0):
			self.texture =textures["level.png"]
		else: self.texture =textures["level2.png"]
		# 
		
		# self.texture = textures[texture]
		self.x, self.y = x, y
		self.tiles = self.init_tiles(self.x, self.y)
		if load_immediately: self.load_tiles()



	def init_tiles(self, room_x=0, room_y=0):
	#Create the QUICK data for the Tile. (NO Sprites!)

		#Consider the ROOM OFFSET.
		tiles = []
		w, h = RENDER_WIDTH/GRID, RENDER_HEIGHT/GRID
		room_x *= RENDER_WIDTH/GRID
		room_y *= RENDER_HEIGHT/GRID

		for x in range(w):
			tiles.append([])
			for y in range(h):
				tile = self.Tile(self.texture)
				tile.x, tile.y = room_x+x, room_y+y
				tiles[-1].append(tile)
		return tiles


	def load_tiles(self): #(unused by WorldMap)
	#Create the SLOW data for the Tile. (Sprite)
		for x in self.tiles:
			for tile in x:
				tile.load()

	def draw(self):
		for x in self.tiles:
			for y in x:
				y.draw()


	# TILE

	class Tile(object):

		def __init__(self, texture):
			self.sprite = None
			self.texture = texture
			self._position_init()


		# SPRITE HANDLING

		def load(self):
			if self.sprite == None:
				self.sprite = MySprite(self.texture)
				self.sprite.clip.set(GRID,GRID)
				self._sync_sprite() #

		def draw(self):
			if self.sprite != None:
				self.sprite.draw()


		# POSITION
		# Saved as an absolute value.
		# Returned as a grid value.

		def _position_init(self):
			self._x, self._y = 0, 0

		def _sync_sprite(self):
			#Update the sprite with every position change.
			if self.sprite != None:
				self.sprite.goto = self._x, self._y

		@property
		def x(self): return self._x/GRID
		@x.setter
		def x(self, x):
			self._x = x*GRID
			self._sync_sprite()
		#
		@property
		def y(self): return self._y/GRID
		@y.setter
		def y(self, y):
			self._y = y*GRID
			self._sync_sprite()


####

class WorldMap:
#Loads MULTIPLE ROOMS.
#Provides shorthands for accessing all the rooms as one.
	
	def __init__(self, x=None, y=None):
	#Load all of the ROOMS.
		if x == None: x = 1
		if y == None: y = 1
		self.rooms = self._init_rooms(x, y)
		self.init_tile_access()



	# ROOM LOADING
	#Initializes all QUICK data.
	#Gradually loads all SLOW data.

	def _init_rooms(self, w=0, h=0): #(init)
	#Specify the AMOUNT of rooms to be initialized.
		rooms = []
		for x in range(w):
			rooms.append([])
			for y in range(h):
				room = Room(x,y, load_immediately=False)
				rooms[-1].append(room)
		return rooms

	#* Loading is handled in draw.

	def draw(self, camera=None):
	#Draws all of the ROOMS in the game.
	#! Draw only ROOMS shown by a Camera.

		if camera == None:
			x1, x2 = 0, self.tiles_w
			y1, y2 = 0, self.tiles_h
		else:
			x1, x2 = camera.tile_x1, camera.tile_x2
			y1, y2 = camera.tile_y1, camera.tile_y2 
			if x1 < 0: x1 = 0
			if x2 < 0: x2 = 0
			if y1 < 0: y1 = 0
			if y2 < 0: y2 = 0

		for x in self.tiles[x1:x2]:
			for y in x[y1:y2]:
				y.load()
				y.draw()



	# TILE ACCESS
	# Updated whenether the Rooms' tiles change memory.

	def init_tile_access(self):
		self.tiles = []
		
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
				
				self.tiles.append(column)

	@property
	def tiles(self):
	#An xy-list of the tiles of every single room.
		return self._tiles


	# DEBUG

	@property
	def tiles_w(self): return len(self.tiles)
	@property
	def tiles_h(self): return len(self.tiles[0])
	@property
	def tiles_amt(self): return self.tiles_w*self.tiles_h

	@property
	def rooms_w(self): return len(self.rooms)
	@property
	def rooms_h(self): return len(self.rooms[0])
	@property
	def rooms_amt(self): return self.rooms_w*self.rooms_h

####

worldmap = WorldMap(30,30)
print "WorldMap INITIALIZED."

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
	worldmap.draw(Camera)
	#


	window.display()