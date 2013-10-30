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
	
	def __init__(self, Player, WorldMap, Timer):

		self.WorldMap = WorldMap #worldmap reactions
		self.room_size = WorldMap.room_w, WorldMap.room_h

		#####

		self.Player = Player
		self.WorldMap = WorldMap
		self.Timer = Timer

		#####

		self.rooms = []
		self._init(*self.room_size)

		args = Player, WorldMap, Timer
		self._load(args)


	def draw(self, camera):
	#Draw all of the entity rooms.
		self._render(camera)
		#
		for column in self.rooms:
			for room in column:
				room.draw()


	def react(self):
	#! checks ALL of the rooms in existence.
		for column in self.rooms:
			for room in column:
				room.react()
	#

	def _init(self, room_w, room_h): #init
	#Make space for the entity rooms.
		for x in range(room_w):
			self.rooms.append([])
			for y in range(room_h):
				self.rooms[-1].append(None)

	def _load(self, args): #init
	#Prompt the entity rooms to load.
		for x, column in enumerate(self.rooms):
			for y, room in enumerate(column):
				new_args = (x,y) + args
				room = entity_room(new_args)
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

		#bound
		rx, ry, tx, ty = room_x, room_y, tile_x, tile_y
		rx, ry = self.keep_in_room_points((rx, ry))
		tx, ty = self.keep_in_tile_points((tx, ty))
		return rx, ry, tx, ty
	#
	def create(self, name, x, y): #editor
		rx, ry, tx, ty = self._global_to_room_tile(x,y)

		args = name, tx,ty, \
		self.Player,self.WorldMap,self.Timer
		self.rooms[rx][ry].create(args)
	#
	def remove(self, x, y): #editor
		rx, ry, tx, ty = self._global_to_room_tile(x,y)
		self.rooms[rx][ry].remove(tx, ty)


	def save(self): #level_editor general controls

		# Is saving allowed?
		for column in self.rooms:
			for room in column:
				if room.can_save() == False:

					print "! ERROR: Entities NOT saved."
					return

		# Save everything.
		i = 0
		for column in self.rooms:
			for room in column:
				room.save()
				i += 1
		msg = "Entities saved: %s Room(s)" % i
		print msg



class entity_room(GameRectangle):
# * LOADS all of the entities in a room.
# * SAVES all of the entities in a room (editor).

	def __init__(self, args):
		room_x, room_y, Player, WorldMap, Timer = args

		self.room_x, self.room_y = room_x, room_y
		self._init()
		self._load(args)


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


	def react(self): #entities
		for entity in self.entities:
			entity.react()

	#

	def _init(self): #init
		self.entities = []

	def _load(self, args): #init
	# Load a unique .TXT file with names and positioning.
	# Positioning is now in TILES.
		room_x, room_y = self.room_x, self.room_y

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
			new_args = (name, x+ox, y+oy) + args[2:]
			self._create(new_args)

	#

	from tile_key import tile_key
	from tile_lock import tile_lock
	from timer_start import timer_start
	from timer_stop import timer_stop

	def _create(self, args): #load
		x, y = args[1], args[2]

		#if that spot isn't taken
		for entity in self.entities:
			if entity.tile_x == x\
			and entity.tile_y == y:
				return

		#add it
		name = args[0]
		entity_class = getattr(self,name)
		new_entity = entity_class(args)
		self.entities.append(new_entity)


	#########

	# LEVEL EDITOR


	def create(self, args): #entities w/ editor
		#Create an entity in the selected tile.
		self._create(args)

	def remove(self, x, y): #entities w/ editor
		to_delete = None

		#find the value to delete
		for e, entity in enumerate(self.entities):
			if entity.tile_x == x\
			and entity.tile_y == y:
				
				to_delete = self.entities[e]

		if to_delete == None: return

		#delete from both lists
		# room
		self.entities \
		= [i for i in self.entities if i != to_delete]

		# total entities
		from code.game.entities.entity import entity
		name = to_delete.name
		entities = entity.__all__[name]
		entities \
		= [i for i in entities if i != to_delete]
		entity.__all__[name] = entities

		# give total entities new ids
		for i, entity in enumerate(entity.__all__[name]):
			entity.id = i


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

	def can_save(self): #entities.save
		for entity in self.entities:
			if entity.can_save() == False:

				msg = "! %s at %s has STOPPED saving."\
				% (entity.name, entity.tile_position)

				print msg

				return False

		return True

	#