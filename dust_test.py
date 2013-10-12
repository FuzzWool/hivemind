from code.pysfml_game import quit, window, key, sf
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0
#########################################################


#### PARTICLE GENERATOR testing.
from code.pysfml_game import MyTexture, MySprite
from random import randint as random_int

class Particle_Generator:
#Makes lots of little particles.
#Has a few handy presets.

	def __init__(self):
		self.particles = []

	def create(self, amt=1, area=(0,0,0,0)):
	#Randomly speckle the sprites within an area.
		
		texture = MyTexture("assets/effects/dust.PNG")
		for i in range(amt):
			sprite = MySprite(texture)
			sprite.clip.set(10,10)

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

			self.particles.append(sprite)


	def draw(self):
		self._play()
		for particle in self.particles:
			particle.draw()

	#

	def _play(self): #draw
		pass


####

pg = Particle_Generator()

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pg.create(area=(100,100,120,120))

	key.reset_all()

	#Video
	window.clear(sf.Color(255,200,200))
	window.view = Camera
	pg.draw()
	window.display()