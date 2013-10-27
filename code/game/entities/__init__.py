def key(x,y):
#Generates a key string.
	x,y = str(x),str(y)
	if len(x) == 1: x = "0"+x
	if len(y) == 1: y = "0"+y
	return x+y


#####
# entities > entity_room > entity

# It obeys this model for the sake of
# easier positioning for loading,
# and consistency with WorldMap.

# All the sub-files are worked with in creation.

#####

from code.pysfml_game import GameRectangle
#
from code.pysfml_game import GRID
from code.pysfml_game import ROOM_WIDTH
from code.pysfml_game import ROOM_HEIGHT


class entities(GameRectangle):
# * Holds all of the GAME'S entities in ROOMS.
	
	def __init__(self, room_w, room_h):
		self.room_w, self.room_h = room_w, room_h

		self.rooms = []
		self._init(room_w, room_h)
		self._load()

	def draw(self, camera):
	#Draw all of the entity rooms.
		self._render(camera)
		#
		for column in self.rooms:
			for room in column:
				room.draw()

	#

	def _init(self, room_w, room_h): #init
	#Make space for the entity rooms.
		for x in range(room_w):
			self.rooms.append([])
			for y in range(room_h):
				self.rooms[-1].append(None)

	def _load(self): #init
	#Prompt the entity rooms to load.
		for x, column in enumerate(self.rooms):
			for y, room in enumerate(column):
				room = entity_room(x,y)
				self.rooms[x][y] = room

	####

	def _render(self, camera): #draw
	#Prompt the entity rooms to render.
	#Check any rooms on-screen.

		#range
		points = camera.room_points
		x1,y1,x2,y2 = points
		points = x1,y1,x2+1,y2+1
		points = self.keep_in_room_points(points)
		x1,y1,x2,y2 = points

		#do it
		for column in self.rooms[x1:x2]:
			for room in column[y1:y2]:
				room.render(camera)


	####

	# LEVEL EDITOR

	def _global_to_room_tile(self, x, y): #create, remove
	#Create a new entity in the selected tile.

		# Since there's no tile list,
		# a global tile_pos has to be dissected
		# into global rooms and local tile_pos
		tile_x, tile_y = x, y

		#get
		x *= GRID; y *= GRID #abs
		room_x = int(x/ROOM_WIDTH)
		room_y = int(y/ROOM_HEIGHT)

		# tile_x = x
		# while tile_x >= ROOM_WIDTH:
			# tile_x -= ROOM_WIDTH
		# tile_x = int(tile_x/GRID)

		# tile_y = y
		# while tile_y >= ROOM_HEIGHT:
			# tile_y -= ROOM_HEIGHT
		# tile_y = int(tile_y/GRID)

		#bound
		rx, ry, tx, ty = room_x, room_y, tile_x, tile_y
		rx, ry = self.keep_in_room_points((rx, ry))
		tx, ty = self.keep_in_tile_points((tx, ty))
		return rx, ry, tx, ty
	#
	def create(self, name, x, y): #editor
		rx, ry, tx, ty = self._global_to_room_tile(x,y)
		self.rooms[rx][ry].create(name, tx,ty)
	#
	def remove(self, x, y): #editor
		rx, ry, tx, ty = self._global_to_room_tile(x,y)
		self.rooms[rx][ry].remove(tx, ty)


	def save(self): #level_editor general controls
		i = 0
		for column in self.rooms:
			for room in column:
				room.save()
				i += 1
		msg = "%s Rooms(s) saved. (Entities)" % i
		print msg



class entity_room(GameRectangle):
# * LOADS all of the entities in a room.
# WIP - SAVES all of the entities in a room (editor).

	def __init__(self, room_x, room_y):
		self.room_x, self.room_y = room_x, room_y
		self._init()
		self._load(room_x, room_y)


	def draw(self): #entities
		for entity in self.entities:
			entity.draw()

	def render(self, camera): #entities
	#Render any entities within absolute bounds.
	#Unrender otherwise.
		points = camera.points

		for entity in self.entities:

			if entity.in_points(points):
				if entity.sprite == None:
					entity.render()
			else:
				entity.sprite = None

	#

	def _init(self): #init
		self.entities = []

	def _load(self, room_x, room_y): #init
	# Load a unique .TXT file with names and positioning.
	# Positioning is now in TILES.
		
		#Grab
		global key
		k = key(room_x, room_y)
		directory = "assets/entities/unique/%s.txt" % k

		try:
			f = open(directory, "r")
			data = f.read()
		except:
			f = open(directory, "w+")
			data = ""

		f.close()
		if data == "": return

		#Interpret
		split_data = data.split("\n")
		
		for line in split_data:
			
			#values
			split_line = line.split(",")
			name = split_line[0]
			x = int(split_line[1][0:2])
			y = int(split_line[1][2:4])

			#offset
			ox = int((room_x*ROOM_WIDTH)/GRID)
			oy = int((room_y*ROOM_HEIGHT)/GRID)

			#Create
			self._create(name, x+ox, y+oy)

	#

	from tile_key import tile_key

	def _create(self, name, x, y): #load

		#if that spot isn't taken
		for entity in self.entities:
			if entity.tile_x == x\
			and entity.tile_y == y:
				return

		#add it
		entity_class = getattr(self,name)
		new_entity = entity_class(name, x, y)
		self.entities.append(new_entity)


	#########

	# LEVEL EDITOR


	def create(self, name, x, y): #entities w/ editor
	#Create an entity in the selected tile.
		self._create(name,x,y)

	def remove(self, x, y): #entities w/ editor

		for e, entity in enumerate(self.entities):
			if entity.tile_x == x\
			and entity.tile_y == y:
				
				del self.entities[e]


	def save(self): #entities w/ editor
	# Save all of the entities back back to room .TXT.
		
		global key

		#Grab
		data = ""
		for entity in self.entities:

			#pos offset
			ox = int((self.room_x*ROOM_WIDTH)/GRID)
			oy = int((self.room_y*ROOM_HEIGHT)/GRID)

			#values
			name = entity.name
			x, y = entity.tile_position
			k = key(x-ox,y-oy)
			#
			data = data + name+","+k+"\n"
		
		if data != "": data = data[:-1]
		

		#Save
		k = key(self.room_x, self.room_y)
		directory = "assets/entities/unique/%s.txt" % k

		f = open(directory,"w+")
		f.write(data)
		f.close()

	#