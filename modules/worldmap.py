from modules import Level

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
	#Make only the slots needed for loading the levels.
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
				new_Room = Level(a1+a2, x, y)
				# new_Room.room_x = x; new_Room.room_y = y
				self.Rooms[-1].append(new_Room)


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
		x1, y1 = keep_in_bounds(x1, y1)
		x2, y2 = keep_in_bounds(x2, y2)

		#Load any rooms within the range, if they're empty
		#Void any rooms not within the range
		for x in range(self.w):
			for y in range(self.h):

				if x1 <= x <= x2\
				and y1 <= y <= y2:
					if self.Rooms[x][y] == None:
						a1 = self.alphabet[x]
						a2 = self.alphabet[y]
						new_Room = Level(a1+a2, x, y)
						self.Rooms[x][y] = new_Room
					
					self.Rooms[x][y]\
					.load_around(*tile_pos)

				
				elif x < x1 or x2 < x\
				or   y < y1 or y2 < y:
					self.Rooms[x][y] = None

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