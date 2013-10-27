class entity: #inherit, don't use
# * Just grabs the name and position.
	
	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y

	###

	def render(self):
		pass

	def draw(self):
		pass

	###

	def react(self, Player):
		pass