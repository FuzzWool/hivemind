#Make a new ROOM class from scratch.

import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0,0

#####

from code.pysfml_game import\
 RENDER_WIDTH, RENDER_HEIGHT
from code.pysfml_game import GRID



# STATIC - Load ALL of the textures in advance.
textures = {}

import glob
import os
directory = "assets/levels"
os.chdir(directory)
for filename in glob.glob("*.png"):
	texture = MyTexture(filename)
	textures[filename] = texture
os.chdir("../../")
# 

class Room(object):
#Handles TILE positioning and BATCHING.


	def __init__(self, x=0, y=0, texture="level.png"):
		#Grab the Room's POSITION.
		#Grab the TEXTURE for all the sprites.

		# #TEST
		# if (x % 2 == 0 and y % 2 != 0)\
		# or (x % 2 != 0 and y % 2 == 0):
		# 	self.texture =textures["level.png"]
		# else: self.texture =textures["level2.png"]
		# # 
		
		self.texture = textures["level.png"]

		#Logic
		self.x, self.y = x, y
		self.load_room_file()
		self.tiles = self.init_tiles(self.x, self.y)

		#Graphics
		self.vertex_array = self.init_vertex_array()
		self.render_states = sf.graphics.RenderStates()
		self.render_states.texture = self.texture



	# TILE DATA

	def load_room_file(self):
	#Load the TILE DATA from a TEXT FILE.
		
		#load file
		directory = "outside/levels"


		# text_file = open()


	#

	def init_tiles(self, room_x=0, room_y=0): #(init)
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


	# GRAPHICS
	#Create a VERTEX ARRAY carrying all of the
	#TILES in a single drawable. 

	def init_vertex_array(self): #(init)
		shape = sf.PrimitiveType.QUADS
		vertex_array = sf.VertexArray(shape)

		for column in self.tiles:
			for tile in column:
				
				tile.init_vertices()
				for point in tile.vertices:
					vertex_array.append(point)
		return vertex_array

	def draw(self):
		window.draw(self.vertex_array, self.render_states)




	# TILE

	class Tile(object):

		def __init__(self, texture):
			self.texture = texture
			self.vertices = []

			self._position_init()


		# GRAPHIC
		#Coordinates saved for generation by ROOM.

		def init_vertices(self): #Room: init_vertex_array
			#points
			point1 = sf.Vertex()
			point2 = sf.Vertex()
			point3 = sf.Vertex()
			point4 = sf.Vertex()

			#position
			x1, y1 = self.x*GRID, self.y*GRID
			x2, y2 = (self.x+1)*GRID, (self.y+1)*GRID
			point1.position = x1,y1
			point2.position = x2,y1
			point3.position = x2,y2
			point4.position = x1,y2

			#clip
			point1.tex_coords = 0,0
			point2.tex_coords = 0,GRID
			point3.tex_coords = GRID,GRID
			point4.tex_coords = GRID,0

			self.vertices.append(point1)
			self.vertices.append(point2)
			self.vertices.append(point3)
			self.vertices.append(point4)


		# POSITION
		# Saved as an absolute value.
		# Returned as a grid value.

		def _position_init(self):
			self._x, self._y = 0, 0

		@property
		def x(self): return self._x/GRID
		@x.setter
		def x(self, x): self._x = x*GRID
		#
		@property
		def y(self): return self._y/GRID
		@y.setter
		def y(self, y): self._y = y*GRID


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
				room = Room(x,y)
				rooms[-1].append(room)
		return rooms


	def draw(self, camera=None):
	#Draws all of the ROOMS in the game.
	#! Draw only ROOMS shown by a Camera.

		if camera == None:
			x1, x2 = 0, self.rooms_w
			y1, y2 = 0, self.rooms_h
		else:
			x1, x2 = camera.room_x1, camera.room_x2
			y1, y2 = camera.room_y1, camera.room_y2
			if x1 < 0: x1 = 0
			if x2 < 0: x2 = 0
			if y1 < 0: y1 = 0
			if y2 < 0: y2 = 0

		for column in self.rooms[x1:x2]:
			for room in column[y1:y2]:
				room.draw()


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

#30,30
worldmap = WorldMap(1,1)
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