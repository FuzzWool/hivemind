from modules.level_editor import ELevel
from modules.worldmap import WorldMap

class EWorldMap(WorldMap):
#Glues the individual rooms together.
#WorldMap file simply contains coordinates for w, h.

	def load_around(self, room_pos, tile_pos):
	#Load only the rooms within a certain position.

		def keep_in_bounds(x=0, y=0):
			logic_w, logic_h = self.w-1, self.h-1
			if logic_w < x: x = logic_w
			if logic_h < y: y = logic_h
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

				if (x in range(x1, x2+1))\
				and (y in range(y1, y2+1)):
					if self.Rooms[x][y] == None:
						a1 = self.alphabet[x]
						a2 = self.alphabet[y]
						new_Room = ELevel(a1+a2, x, y)
						self.Rooms[x][y] = new_Room
					
					self.Rooms[x][y]\
					.load_around(*tile_pos)

				
				elif (x not in range(x1, x2+1))\
				or (y not in range(y1, y2+1)):
					if self.Rooms[x][y] != None:
						self.Rooms[x][y].save()
						self.Rooms[x][y] = None


	def load_all(self):
	#All of the levels in the map.

		#Load and position the Rooms from data
		for x in range(self.w):
			self.Rooms.append([])
			for y in range(self.h):
				a1 = self.alphabet[x]
				a2 = self.alphabet[y]
				new_Room = ELevel(a1+a2, x, y)
				# new_Room.room_x = x; new_Room.room_y = y
				self.Rooms[-1].append(new_Room)


	def save(self):
	#Save the WorldMap and all it's rooms.
		#WorldMap
		f = open("outside/levels/WorldMap.txt", "w")
		data = "%s,%s" % (self.w, self.h)
		f.write(data)
		f.close()
		
		#Save all rooms which've been opened and closed.
		#WIP
		for x in self.Rooms:
			for y in x:
				if y != None:
					y.save()