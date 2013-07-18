from modules.level_editor import ELevel

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
		self.w, self.h = \
		 [int(i) for i in WorldMap.split(",")]

		#Load and position the Rooms from data
		for x in range(self.w):
			self.Rooms.append([])
			for y in range(self.h):
				a1 = self.alphabet[x]
				a2 = self.alphabet[y]
				self.Rooms[x].append(ELevel(a1+a2))


	def save(self):
	#Save the WorldMap and all it's rooms.
		#WorldMap
		f = open("outside/levels/WorldMap.txt", "w")
		f.write("%s,%s") % (self.w, self.h)
		f.close()

		for x in self.Rooms:
			for y in x:
				y.save()

	def draw(self):
	#Draw all the Rooms.
		for x in self.Rooms:
			for y in x:
				y.draw()