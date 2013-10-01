from code.pysfml_game import MyTexture
from code.pysfml_game import RENDER_WIDTH, RENDER_HEIGHT
from code.pysfml_game import GRID
from code.pysfml_game import sf
from code.pysfml_game import window


# STATIC - Load ALL of the shared assets in advance.
_filenames = []
textures = {}
collisions = {}

import glob
import os
directory = "assets/levels/shared"
os.chdir(directory)

for filename in glob.glob("*.png"):
	texture = MyTexture(filename)
	textures[filename] = texture
	_filenames.append(filename[:-4])

for filename in _filenames:
	
	file_dir = filename+"_collision.txt"
	try:
		f = open(file_dir)
		collision = f.read()
	except:
		#Create default data.
		w, h = RENDER_WIDTH/GRID, RENDER_HEIGHT/GRID
		collision = ""
		for x in range(w):
			if collision != "": collision = collision+"\n"
			for y in range(h):
				collision = collision+"0000"

		#Save it.
		f = open(file_dir, "w+")
		f.write(collision)

	f.close()
	collisions[filename] = collision

os.chdir("../../../")
#

class Room(object):
#Handles TILE positioning and BATCHING.

# * May be positioned in different areas of a WORLD MAP.
# * Can load different TEXTURES.
# * Can load different TILE LAYOUTS.
# !WIP: Can load COLLISION INFORMATION.


	def __init__(self, x=0, y=0, texture=None):
		#Grab the Room's POSITION.
		#Grab the TEXTURE for all the sprites.
		
		#LOGIC
		self.x, self.y = x, y
		self.tiles = self.init_tiles(self.x, self.y)

		#assets
		if not texture: texture = self.load_room_texture()
		self.texture_name = texture
		self.tiles = self.load_tile_data(self.tiles)
		self.tiles = self.load_tile_collisions(self.tiles)

		#GRAPHIC
		self.change_texture(texture, init=True)
		self.render_graphics()



	# Loading TILE DATA

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


	#Load ASSETS

	def key(self):
	#For locating the ROOM in UNIQUE ASSETS.
		x, y = str(self.x), str(self.y)
		if len(x) == 1: x = "0"+x
		if len(y) == 1: y = "0"+y
		return x+y


	def load_room_texture(self): #init
		key = self.key()
		directory = "assets/levels/unique/"
		file_dir = directory+key+"_texture.txt"

		#Open FILE.
		try:
			open_file = open(file_dir, "r")
		except:
			open_file = open(file_dir, "w+")
			open_file.write("level1")

		read_data = open_file.read()
		open_file.close()

		return read_data


	def load_tile_data(self, tiles): #(init)
	#Load the TILE DATA from the UNIQUE ROOM FILE.
		
		#load FILE DATA.
		key = self.key()
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


	def load_tile_collisions(self, tiles): #init
	#Load the COLLISION DATA for each tile.

		#Grab SHARED COLLISION data for the tileset
		#and merge it with UNIQUE POSITIONING.

		file_data = collisions[self.texture_name]

		#format the FILE DATA.
		formatted_data = [[]]
		s = 0
		while s < len(file_data):
			if file_data[s] == "\n":
				s+=1
				formatted_data.append([])
			collision = file_data[s:s+4]
			formatted_data[-1].append(collision)
			s += 4

		#Apply the DATA.
		for x, _x in enumerate(tiles):
			for y, _y in enumerate(tiles[x]):
				
				#Apply collisions based on tile data.
				key = tiles[x][y].data
				if key != "____":
					kx, ky = int(key[0:2]), int(key[2:4])
					collision = formatted_data[kx][ky]
				else:
					collision = "____"
				tiles[x][y].collision = collision

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
	def tiles_x(self): return self.x*self.tiles_w
	@property
	def tiles_y(self): return self.y*self.tiles_h
	@property
	def tiles_h(self): return len(self.tiles[0])
	@property
	def tiles_w(self): return len(self.tiles)



	# ROOM EDITING
	#Functions designed for use by Level Editors.
	#Graphics need to be re-rendered along with changes
	#in logic.

	#level_editor
	def change_tile(self, position=(), data=""):
		x, y = position
		self.tiles[x][y].data = data
		self.render_graphics()

	#init, level_editor
	def change_texture(self, texture,
		init=False):

		directory = "assets/levels/shared/%s.png" \
		% texture

		self.texture_name = texture
		self.texture = MyTexture(directory)
		if not init: self.render_graphics()

	#init, change_tile, change_texture
	def render_graphics(self): 
		self.vertex_array = self.init_vertex_array()
		self.render_states = sf.graphics.RenderStates()
		self.render_states.texture = self.texture

	#

	#level_editor
	def save(self):
		self.save_room_texture()
		self.save_tile_data()
		self.save_collision_data()
	#
	def save_room_texture(self): #save
		key = self.key()
		directory = "assets/levels/unique/"
		file_dir = directory+key+"_texture.txt"
		f = open(file_dir, "w+")
		f.write(self.texture_name)
		f.close()
	#
	def save_tile_data(self): #save

		#grab data
		save_data = ""
		for column in self.tiles:
			if save_data != "":
				save_data = save_data+"\n"
			for tile in column:
				save_data = save_data+tile.data

		#save data to file
		key = self.key()

		directory = "assets/levels/unique/%s.txt" % key
		open_file = open(directory, "w")
		open_file.write(save_data)
		open_file.close()
	#
	def save_collision_data(self): #save
		pass




	# TILE

	class Tile(object):

		def __init__(self):
			self.data = "____"
			self.collision = "____"
			
			self._position_init()
			self.vertices = []
			


		# GRAPHIC
		#Coordinates saved for generation by ROOM.

		def init_vertices(self): #Room: init_vertex_array
			self.vertices = []

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
					point.tex_coords = 0,0
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