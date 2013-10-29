from entities import entities

########

from code.pysfml_game import MyTexture
from code.pysfml_game import RENDER_WIDTH, RENDER_HEIGHT
from code.pysfml_game import GRID
from code.pysfml_game import sf
from code.pysfml_game import window

from code.pysfml_game import GameRectangle

#tiles
from code.pysfml_game import collision, slope_collision


# STATIC - Load ALL of the shared assets in advance.
class load:
	_filenames = []
	textures = {}

	import glob
	import os
	directory = "assets/levels/shared"
	os.chdir(directory)

	# TEXTURES
	for filename in glob.glob("*.png"):
		texture = MyTexture(filename)
		textures[filename] = texture
		_filenames.append(filename[:-4])


	# COLLISIONS
	collisions, _collisions = {}, {}

	#grab
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
				if collision != "":
					collision = collision+"\n"
				for y in range(h):

					#Make COLLISION-LEVEL default.
					kx, ky = str(x), str(y)
					if len(kx) == 1: kx = "0"+kx
					if len(ky) == 1: ky = "0"+ky
					key = kx+ky
					#

					#key = "0000"
					collision = collision+key

			#Save it.
			f = open(file_dir, "w+")
			f.write(collision)

		f.close()
		_collisions[filename] = collision


	#format
	for key in _collisions:

		file_data = _collisions[key]

		formatted_data = [[]]
		s = 0
		while s < len(file_data):
			if file_data[s] == "\n":
				s+=1
				formatted_data.append([])
			collision = file_data[s:s+4]
			formatted_data[-1].append(collision)
			s += 4

		collisions[key] = formatted_data


	os.chdir("../../../")
#

class Room(GameRectangle):
#Handles TILE positioning and BATCHING.

# * May be positioned in different areas of a WORLD MAP.
# * Can load different TEXTURES.
# * Can load different TILE LAYOUTS.
# * Can load COLLISION INFORMATION.
# * Can load CAMERA LOCKS.


	def __init__(self, x=0, y=0, texture=None):
		#Grab the Room's POSITION.
		#Grab the TEXTURE for all the sprites.
		
		#GameRectangle
		self.x, self.y = x*RENDER_WIDTH, y*RENDER_HEIGHT
		self.w, self.h = RENDER_WIDTH, RENDER_HEIGHT

		#

		key = self.key()
		w,h = self.tile_w, self.tile_h

	
		self.tiles\
		= self.init_tiles(self.room_x, self.room_y)
		
		tiles = self.tiles
		
		self.layout = self._layout(key,tiles)
		self.graphics = self._graphics(texture,key,tiles)
		
		texture_n = self.graphics.texture_name
		self.collision = self._collision(tiles,texture_n)

		self.camera_locks = self._Camera_Locks(key)



	def draw(self): self.graphics.draw()


	#######

	class _layout:
	# * Generates the layout of all of the tiles.

		def __init__(self, key, tiles):
			self.key = key
			self.tiles = tiles
			#
			self.load()


		def load(self): #init
		#Load the TILE DATA from the UNIQUE ROOM FILE.
			
			key = self.key
			tiles = self.tiles
			tiles_w = len(self.tiles)
			tiles_h = len(self.tiles[0])

			#load FILE DATA.
			directory = "assets/levels/unique/"
			location = directory+key+".txt"
			try:
				f = open(location,"r+")
				file_data = f.read()
			except:
				#Create DATA to use.
				file_data = ""
				for x in range(tiles_w):
					column = "____"*tiles_h
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
					tiles[x][y].data \
					= formatted_data[x][y]

			return tiles



	#######

	class _graphics:
	# * Creates a single VERTEX ARRAY which contains
	# the graphics of all the TILES. 

		vertex_array = None
		render_states = None
		texture = None
		texture_name = None

		def __init__(self, texture, key, tiles):
			self.tiles = tiles

			self.key = key
			self.texture_name = self._load_texture()
			self.texture \
			= load.textures[self.texture_name+".png"]

			self.vertex_array =self._init_vertex_array()
			self.render()


		def _load_texture(self): #init

			directory = "assets/levels/unique/"
			file_dir = directory+self.key+"_texture.txt"

			#Open FILE.
			try:
				open_file = open(file_dir, "r")
				read_data = open_file.read()
			except:
				open_file = open(file_dir, "w+")
				open_file.write("level1")
				read_data = "level1"

			open_file.close()

			return read_data


		def _init_vertex_array(self): #init
			shape = sf.PrimitiveType.QUADS
			vertex_array = sf.VertexArray(shape)

			for column in self.tiles:
				for tile in column:
					
					tile.init_vertices()
					for point in tile.vertices:
						vertex_array.append(point)
			return vertex_array


		#init, change_tile, change_texture
		def render(self):
			self.vertex_array =self._init_vertex_array()
			self.render_states =sf.graphics.RenderStates()
			self.render_states.texture =self.texture


		def draw(self): #_.draw
			window.draw\
			(self.vertex_array, self.render_states)



	#######

	class _collision:
	# * Applies COLLISIONS to all of the tiles.

		def __init__(self, tiles, texture_name):
			self.texture_name = texture_name
			self.tiles = tiles
			#
			self.load()


		def load(self): #init
		#Load the COLLISION DATA for each tile.

			tiles = self.tiles
			texture_name = self.texture_name

			#Grab SHARED COLLISION data for the tileset
			#and merge it with UNIQUE POSITIONING.
	
			file_data = load.collisions[texture_name]

			#Apply the DATA.
			for x, _x in enumerate(tiles):
				for y, _y in enumerate(tiles[x]):
					
					#Apply collisions based on tile data.
					key = tiles[x][y].data
					if key != "____":
						kx, ky \
						= int(key[0:2]), int(key[2:4])
						collision\
						 = load.collisions\
						 [texture_name][kx][ky]
					else:
						collision = "____"

					tiles[x][y].apply_collision(collision)


	#######


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
				tile = self.Tile(self)
				tile.x = (room_x+x)*GRID
				tile.y = (room_y+y)*GRID
				tiles[-1].append(tile)
		return tiles


	#Load ASSETS

	def key(self):
	#For locating the ROOM in UNIQUE ASSETS.
		x, y = str(self.room_x), str(self.room_y)
		if len(x) == 1: x = "0"+x
		if len(y) == 1: y = "0"+y
		return x+y



	# ROOM EDITING
	#Functions designed for use by Level Editors.
	#Graphics need to be re-rendered along with changes
	#in logic.

	#level_editor
	def change_tile(self, position=(), data=""):
		x, y = position
		self.tiles[x][y].data = data
		self.graphics.render()

	#init, level_editor
	def change_texture(self, texture,
		init=False):

		directory = "assets/levels/shared/%s.png" \
		% texture

		self.graphics.texture_name = texture
		self.graphics.texture = MyTexture(directory)
		if not init: self.graphics.render()

	#

	#level_editor
	def save(self):
		self.save_room_texture()
		self.save_tile_data()
		self.save_collision_data()
		self.camera_locks.save()
	#
	def save_room_texture(self): #save
		key = self.key()
		directory = "assets/levels/unique/"
		file_dir = directory+key+"_texture.txt"
		f = open(file_dir, "w+")
		f.write(self.graphics.texture_name)
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

	######


	class _Camera_Locks:
	#Loads the camera boundaries: the camera locks.
		
		#_LOAD
		#Loads values from a text file.

		def __init__(self, key): #Room.init
			self.key = key
			self._load()
		#
		def _load(self): #init
			d = "assets/levels/unique/"+\
			self.key+"_camera_locks.txt"

			try:
				f = open(d,"r")
				r = f.read()
			except:
				f = open(d,"w+")
				r = "0000"
				f.write(r)
			f.close()
			#

			self.left = bool(r[0] == "1")
			self.right = bool(r[1] == "1")
			self.up = bool(r[2] == "1")
			self.down = bool(r[3] == "1")
			

		#PROPERTIES
		left, right, up, down = False, False, False, False

		#SAVE
		#Saves values to a text file.
		def save(self): #level_editor

			to_save = \
			str(int(self.left))+str(int(self.right))+\
			str(int(self.up))+str(int(self.down))

			d = "assets/levels/unique/"+\
			self.key+"_camera_locks.txt"
			f = open(d,"w+")
			f.write(to_save)
			f.close()



	######





	# TILE

	class Tile(GameRectangle):

		def __init__(self, room):
			self.x, self.y = 0, 0
			self.w, self.h = GRID, GRID
			self._ = room #used by: change
			#
			self.data = "____"
			self.vertices = []

			self.init_collision()
		

		# EDITING

		def change(self, new_data): #debugging
		#data, collision, graphics

			self.data = new_data
			self._update_collision()
			self._.graphics.render()


		def _update_collision(self): #change
			key = self.data
			if key != "____":
				kx, ky = int(key[0:2]), int(key[2:4])
				collision\
				 = load.collisions\
				 [self._.graphics.texture_name][kx][ky]
			else:
				collision = "____"
			self.apply_collision(collision)


		# COLLISION
		#Stores generic collision information.

		def init_collision(self): #init
			self.collision_data = "____"
			self.collision = collision(self)
			self.slope_collision = slope_collision(self)


		def apply_collision(self, data):
		#Apply slope specific bindings if needed.
			self.collision_data = data
				
			x1, x2 = self.x1, self.x2
			y1, y2 = self.y1, self.y2
			xc, yc = self.center

			anchor = None

			#ONE-TILE SLOPES
			if data == "0100":
				a,b = (x2, y1),(x1, y2)
				anchor = "rd"
			if data == "0200":
				a,b = (x1, y1),(x2, y2)
				anchor = "ld"
			if data == "0101":
				a,b = (x2, y2),(x1, y1)
				anchor = "ru"
			if data == "0201":
				a,b = (x1, y2),(x2, y1)
				anchor = "lu"

			#TWO-TILE SLOPES
			#horizontal
			if data == "0300":
				a,b = (x1, y2),(x2, yc)
				anchor = "rd"
			if data == "0400":
				a,b = (x2, y1),(x1, yc)
				anchor = "rd"

			if data == "0500":
				a,b = (x2, y1),(x1, yc)
				anchor = "ld"
			if data == "0600":
				a,b = (x2, yc),(x1, y2)
				anchor = "ld"

			if data == "0301":
				a,b = (x1, y1),(x2, yc)
				anchor = "ru"
			if data == "0401":
				a,b = (x1, yc),(x2, y2)
				anchor = "ru"

			if data == "0501":
				a,b = (x2, yc),(x1, y2)
				anchor = "lu"
			if data == "0601":
				a,b = (x2, y1),(x1, yc)
				anchor = "lu"

			# #vertical
			# if data == "ec":
			# 	a, b = (x2, y1),(xc, y2)
			# 	anchor = "rd"
			# if data == "ed":
			# 	a, b = (xc, y1),(x1, y2)
			# 	anchor = "rd"

			# if data == "ee":
			# 	a, b = (x1, y1),(xc,y2)
			# 	anchor = "ru"
			# if data == "ef":
			# 	a,b = (xc,y1),(x2,y2)
			# 	anchor = "ru"

			# if data == "fc":
			# 	a, b = (x1,y1),(xc,y2)
			# 	anchor = "ld"
			# if data == "fd":
			# 	a,b = (xc,y1),(x2,y2)
			# 	anchor = "ld"

			# if data == "fe":
			# 	a,b = (x2,y1),(xc,y2)
			# 	anchor = "lu"
			# if data == "ff":
			# 	a,b = (xc, y1),(x1, y2)
			# 	anchor = "lu"
			#

			if anchor:
				self.slope_collision.a = a
				self.slope_collision.b = b
				self.slope_collision.anchor = anchor

			#Define SIDE PROPERTIES. (wall-jumping)



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
			x1, y1, x2, y2 = self.points
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
		x,y,w,h = 0,0,0,0

		#STATES

		def is_empty(self):
			return bool(self.data == "____")