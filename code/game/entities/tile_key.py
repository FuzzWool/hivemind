from code.game.entities.entity import entity

from code.pysfml_game import MyTexture, MySprite
from code.pysfml_game import GameRectangle
from code.pysfml_game.animation import oscillate



class tile_key(entity):
# * Bobs up and down.
# * 'Collected' on contact with Nut.
# WIP - Opens up an assigned tile_lock.

	def __init__(self, name, tile_x, tile_y):
		entity.__init__(self, name, tile_x, tile_y)
		self._init_cbox()

	##

	def render(self): #entity_room
		if not self.collected:
			entity.render(self)
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


	##########

	def can_save(self):
	#Has to have a matching LOCK.

		keys = entity.__all__["tile_key"]
		locks = entity.__all__["tile_lock"]
		try: locks[self.id]
		except:
			print "! Key has no Lock with the same ID."
			print "Keys: ",[k.id for k in keys]
			print "Locks: ",[l.id for l in locks]

			return False

		return True