from code.pysfml_game import GameRectangle
from code.pysfml_game import MyTexture, MySprite

class tile_lock(GameRectangle):
# * Just grabs the name and position.
	
	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y

		self.w, self.h = 25, 25
		self.sprite = None

	###

	def render(self):
		d = "assets/entities/shared/tile_lock/sheet.png"
		t = MyTexture(d)
		sprite = MySprite(t)
		sprite.position = self.position
		#
		self.sprite = sprite

	def draw(self):
		if self.sprite != None:
			self.sprite.draw()

	###

	def react(self, Player):
		pass