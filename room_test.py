#Make a new ROOM class from scratch.

import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0,0

#####

from code.pysfml_game import\
 RENDER_WIDTH, RENDER_HEIGHT
from code.pysfml_game import GRID



# STATIC - Load ALL of the textures in advance.
textures = {}

import glob
import os
directory = "assets/levels/same"
os.chdir(directory)
for filename in glob.glob("*.png"):
	texture = MyTexture(filename)
	textures[filename] = texture
os.chdir("../../../")
# 

class Room(object):
#Handles TILE positioning and BATCHING.

# * May be positioned in different areas of a WORLD MAP.
# * Can load different TEXTURES.
# ! Can load different TILE LAYOUTS.


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
		self.tiles = self.init_tiles(self.x, self.y)
		self.tiles = self.load_tile_data(self.tiles)

		#Graphics
		self.vertex_array = self.init_vertex_array()
		self.render_states = sf.graphics.RenderStates()
		self.render_states.texture = self.texture



	# TILE DATA

	def load_tile_data(self, tiles): #(init)
	#Load the TILE DATA from the UNIQUE ROOM FILE.
		
		#find KEY.
		x, y = str(self.x), str(self.y)
		if len(x) == 1: x = "0"+x
		if len(y) == 1: y = "0"+y
		key = x+y

		#load FILE DATA.
		directory = "assets/levels/unique/"
		location = directory+key+".txt"
		try:
			f = open(location,"r+")
			file_data = f.read()
		except:
			#Create DATA to use.
			file_data = ""
			for x in range(self.tiles_w):
				column = "____"*self.tiles_h
				file_data = file_data + column + "\n"
			file_data = file_data[:-1]


			f = open(location,"w")
			f.write(file_data)
		f.close()

		#format FILE DATA for use as a GRID.
		formatted_data = [[]]

		s = 0
		while s < len(file_data):
			if file_data[s] == "\n":
				s += 1
				formatted_data.append([])
			tile = file_data[s:s+4]
			formatted_data[-1].append(tile)
			s += 4

		#apply to all TILES.
		for x, _x in enumerate(tiles):
			for y, _y in enumerate(tiles[x]):
				tiles[x][y].data = formatted_data[x][y]

		return tiles


	#

	def init_tiles(self, room_x=0, room_y=0): #(init)
	#Create EMPTY SLOTS for the tiles...

		#Consider the ROOM OFFSET.
		tiles = []
		w, h = RENDER_WIDTH/GRID, RENDER_HEIGHT/GRID
		room_x *= RENDER_WIDTH/GRID
		room_y *= RENDER_HEIGHT/GRID

		for x in range(w):
			tiles.append([])
			for y in range(h):
				tile = self.Tile()
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


	#POSITION

	@property
	def tiles_h(self): return len(self.tiles[0])
	@property
	def tiles_w(self): return len(self.tiles)



	# TILE

	class Tile(object):

		def __init__(self):
			self.data = "0000" #clip in xxyy format
			self._position_init()
			
			self.vertices = []


		# GRAPHIC
		#Coordinates saved for generation by ROOM.

		def init_vertices(self): #Room: init_vertex_array
			#points
			point1 = sf.Vertex()
			point2 = sf.Vertex()
			point3 = sf.Vertex()
			point4 = sf.Vertex()
			points = [point1,point2,point3,point4]

			#position
			x1, y1 = self.x*GRID, self.y*GRID
			x2, y2 = (self.x+1)*GRID, (self.y+1)*GRID
			point1.position = x1,y1
			point2.position = x2,y1
			point3.position = x2,y2
			point4.position = x1,y2

			#clip
			if not self.is_empty():
				clip_x = int(self.data[0:2])
				clip_y = int(self.data[2:4])

				x1 = (clip_x+0)*GRID
				y1 = (clip_y+0)*GRID
				x2 = (clip_x+1)*GRID
				y2 = (clip_y+1)*GRID

				point1.tex_coords = x1,y1
				point2.tex_coords = x2,y1
				point3.tex_coords = x2,y2
				point4.tex_coords = x1,y2

			else:
				for point in points:
					point.color = sf.Color(0,0,0,0)

			for point in points:
				self.vertices.append(point)

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

		#STATES

		def is_empty(self):
			return bool(self.data == "____")


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