from code.pysfml_game import GameRectangle
from code.pysfml_game import GRID
from code.pysfml_game import ROOM_WIDTH, ROOM_HEIGHT
from code.game import Room

class WorldMap(GameRectangle):
#Loads MULTIPLE ROOMS.
#Provides shorthands for accessing all the rooms as one.
	
	def __init__(self, x=None, y=None):
	#Load all of the ROOMS.
		if x == None: x = 1
		if y == None: y = 1
		self.rooms = self._init_rooms(x, y)
		self.init_tile_access()


	# ROOM LOADING

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
	#Draw only ROOMS shown by a Camera.

		if camera == None:
			x1, x2 = 0, self.room_w
			y1, y2 = 0, self.room_h
		else:
			x1, y1, x2, y2 = camera.room_points
			x2 += 1; y2 += 1
			x1,x2 = self.keep_in_room_x((x1,x2))
			y1,y2 = self.keep_in_room_y((y1,y2))


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


	# LEVEL EDITING

	#level_editor
	def save(self):

		for column in self.rooms:
			for room in column:
				room.save()
		print "%s Room(s) saved." \
		% (self.room_w*self.room_h)


	#POSITION

	x,y = 0,0
	@property
	def w(self): return len(self.rooms)*ROOM_WIDTH
	@property
	def h(self): return len(self.rooms[0])*ROOM_HEIGHT