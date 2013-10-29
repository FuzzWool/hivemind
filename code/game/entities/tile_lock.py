from code.game.entities.entity import entity
from code.pysfml_game import MyTexture, MySprite

from random import randint as random_int
from code.pysfml_game import particle_generator

class tile_lock(entity):
# * Waits for a tile_key to unlock it.
# * Once so, it removes the tile it is occupying.


	def __init__(self, args):
		entity.__init__(self, args)
		#
		self.locked = True
		self._init_animation()

	####

	def render(self):
		if self.locked:
			entity.render(self)

	def draw(self):
		if self.sprite:
			entity.draw(self)
			self._animate()

			if self.locked:
				self._rocking_animation()

		self.pg.draw()

	def react(self):
		WorldMap = self.WorldMap

		key = entity.__all__["tile_key"][self.id]
		if key.collected and self.locked:
			if self.locked:
				x,y = self.tile_x, self.tile_y
				WorldMap.tiles[x][y].change("____")
				#
				self.locked = False

				#optional
				if self.sprite:
					self._fall_animation()


	#

	def _init_animation(self): #init
		self.pg = particle_generator()

	def _rocking_animation(self): #init
		if self.sprite == None: return

		#randomize axis
		sprite = self.sprite
		number = random_int(0,1)
		choice = [sprite.animation.x, sprite.animation.y]
		animation = choice[number]

		if sprite != None \
		and sprite.animation.x.stopped\
		and sprite.animation.y.stopped:

			#choose correct end point
			end_choice = [self.x, self.y]
			animation.end = end_choice[number]

			#randomize direction
			speed, vel = +0.5, -0.1
			if random_int(0,1) == 1:
				speed, vel = -speed, -vel
			animation.speed = speed
			animation.vel = vel


	def _fall_animation(self): #react
		self.sprite.animation.y.end = self.y1+1000
		self.sprite.animation.y.speed = -4
		self.sprite.animation.y.vel = +0.3

		self.pg.create(10, self.points)

	def _animate(self):
		self.sprite.animation.play()
		if self.locked == False:
			if self.sprite.animation.y.stopped:
				self.sprite = None


	####

	def can_save(self):

		#There's a KEY for every lock.
		locks = entity.__all__["tile_lock"]
		keys = entity.__all__["tile_key"]
		try: keys[self.id]
		except:
			print "! Lock has no Key with the same ID."
			
			print "Locks: ",[l.id for l in locks]
			print "Keys: ",[k.id for k in keys]
			return False

		#The lock is NOT covering a tile.
		x, y = self.tile_position
		tile = self.WorldMap.tiles[x][y]
		if tile.data == "____":
			print "! Lock placed on top of empty tile."
			return False

		return True