from code.pysfml_game import GameRectangle
from code.pysfml_game import MyTexture, MySprite

class entity(GameRectangle): #template
# * Grabs name and position.
# * Assumes a sprite exists for it. Renders and draws it.
# * Uses GameRectangle positioning.

# And most importantly...
# * Provides every single method it's hierachy references.


	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y

		self.w, self.h = 25, 25
		self.sprite = None

	###

	def render(self):
		d = "assets/entities/shared/%s/sheet.png"\
		% self.name
		t = MyTexture(d)
		sprite = MySprite(t)
		sprite.position = self.position
		#
		self.sprite = sprite

	def draw(self):
		if self.sprite != None: self.sprite.draw()

	###

	def react(self, Player):
		pass

	def worldmap_react(self, WorldMap):
		pass