from code.pysfml_game import GameRectangle
from code.pysfml_game import MyTexture, MySprite

class entity(GameRectangle): #template
# * Grabs name and position.

	
	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y

		self.w, self.h = 25, 25
		self.sprite = None

	###

	def render(self):
		pass

	def draw(self):
		pass

	###

	def react(self, Player):
		pass