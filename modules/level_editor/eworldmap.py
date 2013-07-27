from modules.game import WorldMap
from modules.level_editor import ELevel

class EWorldMap(WorldMap):
#Glues the individual rooms together.
#WorldMap file simply contains coordinates for w, h.

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

						#Load a stored room when possible.
						if self.tempRooms[x][y] != None:
							from copy import copy
							r = copy(self.tempRooms[x][y])
							self.Rooms[x][y] = r

						#Otherwise, load afresh.
						else:
							a1 = self.alphabet[x]
							a2 = self.alphabet[y]
							new_Room = ELevel(a1+a2, x, y)
							self.Rooms[x][y] = new_Room
					
					self.Rooms[x][y]\
					.load_around(*tile_pos)

				
				elif x <= x1 or x2 <= x\
				or   y <= y1 or y2 <= y:
					if self.Rooms[x][y] != None:
						# self.Rooms[x][y].save()
						from copy import copy
						oldroom = copy(self.Rooms[x][y])
						self.tempRooms[x][y] = oldroom
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

#	SAVING

	def save(self):
	#Save the WorldMap and all it's rooms.
		#WorldMap
		f = open("outside/levels/WorldMap.txt", "w")
		data = "%s,%s" % (self.w, self.h)
		f.write(data)
		f.close()
		
		rooms = 0
		#Save all rooms which've been opened and closed.
		for x in self.tempRooms:
			for y in x:
				if y != None:
					y.save()
					rooms += 1

		for x in self.Rooms:
			for y in x:
				if y != None:
					y.save()
					rooms += 1

		print "Saved the WorldMap! (%s Rooms saved)"\
		% rooms

	tempRooms = []
	def __init__ (self):
		WorldMap.__init__(self)
		self.tempRooms = [i[:] for i in self.Rooms]