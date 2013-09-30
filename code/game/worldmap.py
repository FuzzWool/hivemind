from code.game import Room

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
