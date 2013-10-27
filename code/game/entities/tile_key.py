from code.pysfml_game import GameRectangle
from code.pysfml_game import MyTexture, MySprite
from code.pysfml_game.animation import oscillate

class tile_key(GameRectangle):
# * Bobs up and down.
# * 'Collected' on contact with Nut.
# WIP - Opens up an assigned tile_lock.

	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y
		self.w, self.h = 25,25
		self.sprite = None

		self._init_cbox()

	##

	def render(self): #entity_room
		if self.collected: return

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
			self._update_cbox()
			self.sprite.draw()



	# ANIMATION

	def _init_animation(self): #render
		self.animation_y = oscillate()
		self.animation_y.speed = +1
		self.animation_y.vel = -0.1
		self.animation_y.end = self.y

	def _animate(self): #draw

		sprite, animation_y = self.sprite, self.animation_y
		sprite.y += animation_y.play(sprite.y)



	# EVENTS

	collected = False

	def _init_cbox(self): #init
		self.cbox = GameRectangle()
		self.cbox.size = 20,10

	def _update_cbox(self): #draw
		self.cbox.center = self.sprite.center

		# #DEBUG
		# import sfml as sf
		# from code.pysfml_game import window
		# rect = sf.RectangleShape()
		# rect.position = self.cbox.position
		# rect.size = self.cbox.size
		# window.draw(rect)
		# #

	def react(self, Player): #entity_room
	#Collected on collision with the player.
		
		if Player.cbox.in_points(self.cbox):
			self.collected = True
			self.sprite = None