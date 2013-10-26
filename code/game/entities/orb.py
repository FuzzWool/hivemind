from code.pysfml_game import GameRectangle
from code.pysfml_game import MyTexture, MySprite

class orb(GameRectangle):
# WIP - Bobs up and down.
# WIP - Explodes on contact with Nut.

	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y

		self._init()


	#

	def _init(self): #init
		self.w, self.h = 10,10
		self.sprite = None

	##

	def render(self): #entity_room
		#Create a MySprite for drawing.
		t = \
		MyTexture("assets/entities/shared/orb/sheet.png")

		sprite = MySprite(t)
		sprite.position = self.x, self.y
		sprite.clip.set(self.w, self.h)
		self.sprite = sprite

	def draw(self): #entity_room
		if self.sprite: self.sprite.draw()