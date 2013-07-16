from modules.level_editor import ELevel

class WorldMap:
#Handles glueing the individual levels together.

	Data = [["level"],["x"],["y"]]
	Levels = [["Level"]]

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
			Level = ELevel(entry[0])
			Level.room_x = int(entry[1])
			Level.room_y = int(entry[2])
			self.Levels.append(Level)


	def save(self):
		pass

	def draw(self):
		for Level in self.Levels:
			Level.draw()