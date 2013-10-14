from code.pysfml_game import quit, window, key, sf
#########################################################
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

#####
#Create an ANIMATION class for MYSPRITE.
from code.pysfml_game import MyTexture, MySprite

class TestSprite(MySprite):
	def __init__ (self, args):
		MySprite.__init__(self, args)

		self.animation_x = axis_animation(self, "x")
		self.animation_y = axis_animation(self, "y")


class axis_animation(object):
#Provides short-hands for calculating easy physics.
#One for each axis: x and y.
	def __init__(self, Rectangle, axis,
		called_directly=True):
		self._ = Rectangle #ugly_move
		self.axis = axis #ugly_move

		#Pre-sets - they subclass this class.
		if called_directly:
			args = Rectangle, axis, False
			self.bounce = bounce(*args)


	#Public

	end = 0
	speed, vel = 0, 0

	def play(self, point):

		if self._passed_end(point, self.speed):
			self.passed_end_event(point)
		self._ugly_move()



	# Overridables

	def passed_end_event(self, point): #void
		self.cut_off(point)

	def cut_off(self, point): #void
		self.speed = self.end - point
		self.vel = 0


	# Private

	def _passed_end(self, point, move): #bool
		return bool(abs(self.end)<= abs(point+move))

	def _ugly_move(self): #void
		if self.axis == "x": self._.x += self.speed
		if self.axis == "y": self._.y += self.speed
		self.speed += self.vel
	#


class bounce(axis_animation):

	vel_divide = 1
	speed_divide = 1

	def passed_end_event(self, point):

		if self.speed != 0:
			
			#Bounce back.
			self.speed = \
			-(self.speed-self.vel/self.speed_divide)
			self.vel = self.vel/self.vel_divide


#####

texture = MyTexture("assets/characters/nut/cbox.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 200,200


def animate():
	sprite.animation_x.bounce.speed = 0
	sprite.animation_x.bounce.vel = 0.5
	sprite.animation_x.bounce.end = 300

	sprite.animation_x.bounce.vel_divide = 0.5

animate()

#

running = True
while running:
	#Logic

	if quit(): running = False
	if key.RETURN.pressed():
		pass

	key.reset_all()

	#Video
	sprite.animation_x.bounce.play(sprite.x)
	# sprite.animation_y.play()
	
	window.clear(sf.Color(0,0,0))
	sprite.draw()
	window.view = Camera
	window.display()