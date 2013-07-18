from modules.level_editor import Level

class WorldMap:
#Glues the individual rooms together.
#WorldMap file simply contains coordinates for w, h.

	w, h = 0, 0
	Rooms = [['Room']]

	alphabet = ["a","b","c","d","e","f","g",\
	 "h","i","j","k","l","m","n","o","p","q",\
	 "q","r","s","t","u","v","w","x","y","z"]

	def __init__ (self):
		self.load()

	def load(self):
	#All of the levels in the map.
		self.w, self.h = 0, 0
		self.Rooms = []

		#Load WorldMap boundary
		f = open("outside/levels/WorldMap.txt")
		WorldMap = f.read()
		f.close()
		WorldMap = WorldMap.split(",")
		self.w = int(WorldMap[0])
		self.h = int(WorldMap[1])

		#Load and position the Rooms from data
		for x in range(self.w):
			self.Rooms.append([])
			for y in range(self.h):
				a1 = self.alphabet[x]
				a2 = self.alphabet[y]
				new_Room = Level(a1+a2)
				new_Room.room_x = x; new_Room.room_y = y
				self.Rooms[-1].append(new_Room)

	def draw(self):
	#Draw all the Rooms.
		for x in self.Rooms:
			for y in x:
				y.draw()