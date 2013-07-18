from modules.level_editor import ELevel

class WorldMap:
#Handles glueing the individual levels together.

	Data = [["level"],["x"],["y"]]
	Levels = [["Level"]]

	def __init__ (self):
		self.load()

	def load(self):
	#For each level, Load the...
	#Filename and x/y Coordinates

		#Load text data
		f = open("outside/levels/WorldMap.txt")
		WorldMap = f.read()
		f.close()

		#Format data to [[level][x][y]]
		WorldMap = WorldMap.split("\n")
		wm = []
		for entry in WorldMap:
			formatted_entry = entry.split(",")
			wm.append(formatted_entry)
		self.Data = [entry[:] for entry in wm]

		#Load and position the Levels from data
		self.Levels = []
		for entry in self.Data:
			name = (entry[0])
			room_x, room_y = int(entry[1]), int(entry[2])
			self.load_Level(name, room_x, room_y)

	def load_Level(self, name, room_x, room_y):
	#Init
	#New Levels in Level Editor Properties
		Level = ELevel(name)
		Level.room_x, Level.room_y = room_x, room_y
		self.Levels.append(Level)


	def save(self):
	#Save the WorldMap and all it's levels.
		#WorldMap
		data = ""
		for Level in self.Levels:
			new_line = "%s,%s,%s" \
			% (Level.name, Level.room_x, Level.room_y)
			data += new_line + "\n"

		f = open("outside/levels/WorldMap.txt", "r+")
		f.write(data[:-1])
		f.close()

		#Levels
		for Level in self.Levels:
			Level.save()

		print "Saved WorldMap!"

	def draw(self):
		for Level in self.Levels:
			Level.draw()

#
	#LevelEditor room removal
	def find_Level(self, room_x, room_y):
	#Find a room based on which area it is locating.
		print room_x, room_y