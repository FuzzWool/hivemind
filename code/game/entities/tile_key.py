from code.pysfml_game import GameRectangle
from code.pysfml_game import MyTexture, MySprite
from code.pysfml_game.animation import oscillate

class tile_key(GameRectangle):
# WIP - Bobs up and down.
# WIP - Explodes on contact with Nut.
# WIP - Opens up an assigned tile_lock.

	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y
		self.w, self.h = 25,25
		self.sprite = None

	##

	def render(self): #entity_room
		#Create a MySprite for drawing.
		t = MyTexture\
		("assets/entities/shared/tile_key/sheet.png")

		sprite = MySprite(t)
		sprite.position = self.x, self.y
		sprite.clip.set(self.w, self.h)
		self.sprite = sprite

		self._init_animation()


	def draw(self): #entity_room

		if self.sprite != None:
			self._animate()
			self.sprite.draw()


	#####

	def _init_animation(self): #render
		self.animation_y = oscillate()
		self.animation_y.speed = +1
		self.animation_y.vel = -0.1
		self.animation_y.end = self.y

	def _animate(self): #draw

		sprite, animation_y = self.sprite, self.animation_y
		sprite.y += animation_y.play(sprite.y)