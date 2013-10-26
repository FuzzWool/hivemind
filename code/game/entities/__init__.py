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

class entities:
# * Holds all of the GAME'S entities in ROOMS.
	
	def __init__(self, room_w, room_h):
		self.rooms = []
		self._init(room_w, room_h)
		self._load()

		self._render()

	def draw(self):
	#Draw all of the entity rooms.
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

	def _render(self): #init
	#Prompt the entity rooms to render.
		for column in self.rooms:
			for room in column:
				room.render()



class entity_room:
# WIP - Loads all of the ENTITIES in a room.
# WIP - Forwards prompts to individual entities.

	def __init__(self, room_x, room_y):
		self._init()
		self._load(room_x, room_y)


	def draw(self): #entities
		for entity in self.entities:
			entity.draw()

	def render(self): #entities
		for entity in self.entities:
			entity.render()


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
			split_line = line.split(",")
			name = split_line[0]
			x = int(split_line[1][0:2])
			y = int(split_line[1][2:4])

			#Create
			self._create(name, x, y)


	#

	from orb import orb

	def _create(self, name, x, y): #load

		entity_class = getattr(self,name)
		new_entity = entity_class(x, y)
		self.entities.append(new_entity)