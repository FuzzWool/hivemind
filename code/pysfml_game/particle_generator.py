from code.pysfml_game import MyTexture, MySprite
from random import randint as random_int
from sfml import Clock

class particle_generator:
#Makes lots of little particles.
#Has a few handy presets.

# WIP - only catered for dust effects.

	def __init__(self):
		self.particles = []

		self.clock = Clock()
		self.interval = 0

	# MAKE (public)

	def create(self, amt=1, area=(0,0,0,0)):
	#Randomly speckle the sprites within an area.
		
		#Only allow it to do so in the proper intervals.
		if self.clock.elapsed_time.seconds < self.interval:
			return

		self.clock.restart()

		#Create the particles.
		texture = MyTexture("assets/effects/dust.PNG")
		for i in range(amt):
			sprite = MySprite(texture)
			sprite.clip.set(10,10)

			#random CLIP
			c = random_int(0,3)
			sprite.clip.use(c,0)

			#Random AREA.
			x1, y1, x2, y2 = area
			x2 -= sprite.w
			y2 -= sprite.h
			if x2 < x1: x2 = x1
			if y2 < y1: y2 = y1

			x = random_int(x1, x2)
			y = random_int(y1, y2)
			sprite.x, sprite.y = x, y
			#

			#animate
			self._jump(sprite)
			self._fade(sprite)
			#

			self.particles.append(sprite)


	def draw(self):
	#Animate, Draw, Delete
		self._play()
		for i, particle in enumerate(self.particles):
			particle.draw()

			if particle.color.a == 0:
				del self.particles[i]


	# ANIMATE

	def _play(self): #draw
		for particle in self.particles:
			particle.animation.play()

	def _jump(self, particle): #create
		speed = 1.0
		s = random_int(10,20)
		s = float(s/10)

		particle.animation.y.speed = -s
		particle.animation.y.vel = 0.1

	def _fade(self, particle): #create
		particle.animation.alpha.vel = -1
