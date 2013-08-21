from modules.game import Room

class WorldMap:
#Glues the individual rooms together.
#WorldMap file simply contains coordinates for w, h.

	w, h = 0, 0
	Rooms = [['Room']]

	alphabet = ["a","b","c","d","e","f","g",\
	 "h","i","j","k","l","m","n","o","p","q",\
	 "q","r","s","t","u","v","w","x","y","z"]

	def __init__ (self):
		self.init_slots()
		# self.load_all()


	def init_slots(self):
	#Make only the slots needed for loading the rooms.
		self.w, self.h = 0, 0
		self.Rooms = []

		#Load WorldMap boundary
		f = open("outside/levels/WorldMap.txt")
		WorldMap = f.read()
		f.close()
		WorldMap = WorldMap.split(",")
		self.w = int(WorldMap[0])
		self.h = int(WorldMap[1])

		#Make Rooms slots.
		for x in range(self.w):
			self.Rooms.append([])
			for y in range(self.h):
				self.Rooms[-1].append(None)

	def draw(self):
	#Draw all the Rooms.
		for x in self.Rooms:
			for y in x:
				if y != None:
					y.draw()

	#

	def load_all(self):
	#All of the levels in the map.

		#Load and position the Rooms from data
		for x in range(self.w):
			self.Rooms.append([])
			for y in range(self.h):
				a1 = self.alphabet[x]
				a2 = self.alphabet[y]
				new_Room = Room(a1+a2, x, y)
				# new_Room.room_x = x; new_Room.room_y = y
				self.Rooms[-1].append(new_Room)


	old_x1, old_y1 = 0, 0
	old_x2, old_y2 = 0, 0
	def load_around(self, room_pos, tile_pos):
	#Load only the rooms within a certain position.

		def keep_in_bounds(x=0, y=0):
			if self.w < x: x = self.w
			if self.h < y: y = self.h
			if x < 0: x = 0
			if y < 0: y = 0
			return x, y

		#Find ROOM positons.
		x1, y1, x2, y2 = room_pos
		x2 += 1; y2 += 1
		x1, y1 = keep_in_bounds(x1, y1)
		x2, y2 = keep_in_bounds(x2, y2)

		#MAKE new ROOMS.
		#Check only the range, nothing outside.
		for x in range(x1, x2):
			for y in range(y1, y2):
				if self.Rooms[x][y] == None:
					a1 = self.alphabet[x]
					a2 = self.alphabet[y]
					new_Room = Room(a1+a2, x, y)
					self.Rooms[x][y] = new_Room

				self.Rooms[x][y].load_around(*tile_pos)

		#DISPOSE of old ROOMS.
		#Grab the last range.
		#None all of it's rooms which
		#aren't also within the new range.
		for x in range(self.old_x1, self.old_x2):
			for y in range(self.old_y1, self.old_y2):

				if  x1 <= x <= x2\
				and y1 <= y <= y2:
					pass
				else:
					self.Rooms[x][y] = None

		self.old_x1, self.old_y1 = x1, y1
		self.old_x2, self.old_y2 = x2, y2


#	DEBUG

	@property
	def Rooms_loaded(self):
	#Returns a list with all of the loaded Rooms.
		loaded = []
		for x in self.Rooms:
			for y in x:
				if y != None:
					loaded.append(y)
		return loaded

	def say_Rooms(self):
	#Prints how many rooms are Loaded.
		total = self.w * self.h
		loaded = len(self.Rooms_loaded)
		string = "(%s/%s) Rooms are loaded."\
		% (loaded, total)
		print string

		for Room in self.Rooms_loaded:
			Room.say_tiles()
		print