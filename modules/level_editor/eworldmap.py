from modules.level_editor import ELevel
from modules.worldmap import WorldMap

class EWorldMap(WorldMap):
#Glues the individual rooms together.
#WorldMap file simply contains coordinates for w, h.


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
				new_Room = ELevel(a1+a2)
				new_Room.room_x = x; new_Room.room_y = y
				self.Rooms[-1].append(new_Room)

	def save(self):
	#Save the WorldMap and all it's rooms.
		#WorldMap
		f = open("outside/levels/WorldMap.txt", "w")
		data = "%s,%s" % (self.w, self.h)
		f.write(data)
		f.close()
		
		for x in self.Rooms:
			for y in x:
				y.save()