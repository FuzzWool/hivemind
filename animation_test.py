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

		self.animation_x = TestAnimation(self, "x")
		self.animation_y = TestAnimation(self, "y")


class TestAnimation:
#Provides short-hands for calculating easy physics.
#One for each axis: x and y.

	def __init__(self, MySprite, axis):
		self._ = MySprite
		self.axis = axis
		self.config = config()


	# PUBLIC

	#Values	
	target = None
	speed, vel = 1,0


	#States - (@property details in private)
	cut_off = True
	bounce = False


	#Method
	def play(self):
	#Move closer to the target.
		self.config.loop_reset()
		position = self.position()

		#Move towards the target.
		if not self.stopped:
			move = self.speed

			#SPECIAL MOVEMENT
			if self._end_passed(move):
				if self.cut_off: move = self.f_cut_off()
				if self.bounce: move = self.m_bounce(move)

			#Speed up.
			self.speed += self.vel

			#Confirm movement.
			if self.axis == "x": self._.move((move, 0))
			if self.axis == "y": self._.move((0, move))


		#Reset
		if self.stopped: self.reset()


	# PRIVATE

	# SPECIAL MOVEMENT

	def _end_passed(self, move): #play
	#True if the end has just been moved passed.
		position = self.position()

		if 0 < move:
			if position <= self.target <= position + move:
				return True

		if move < 0:
			if position + move <= self.target <= position:
				return True

		return False

	def f_cut_off(self): #play
	#Halt the sprite as soon as it reaches the target.
		return self.target - self.position()

	def m_bounce(self, move): #play
	#Bounce the sprite against the 'wall' of the target.
		self.config.bounced = True
		speed_cut = self.config.bounce_speed_cut
		vel_cut = self.config.bounce_vel_cut

		#Bounce back.
		self.speed = -(self.speed/speed_cut)
		self.vel = abs(self.vel/vel_cut)

		#Stop doing this.
		frames_since = self.speed + (self.vel*10)
		if abs(self.speed) < frames_since:
			self.speed = self.f_cut_off()
			self.vel = 0

		move = self.speed
		return move


	# utilities

	def reset(self): #play
	#A complete reset of every single value.
		
		#Values
		self.target = None
		self.speed, self.vel = 1,0
		#
		self._reset_states()
		#
		self.config.full_reset()

	def position(self): #play
		if self.axis == "x": return self._.x
		if self.axis == "y": return self._.y


	# States

	_cut_off = True
	_bounce = False

	def _reset_states(self): #reset, 'states' below
		self._cut_off = False
		self._bounce = False

	@property
	def cut_off(self): return self._cut_off
	@cut_off.setter
	def cut_off(self, truth):
		self._reset_states(); self._cut_off = truth

	@property
	def bounce(self): return self._bounce
	@bounce.setter
	def bounce(self, truth):
		self._reset_states(); self._bounce = truth

	#

	@property
	def stopped(self): #play
		if self.position() == self.target\
		or self.target == None:
			return True
		return False


class config:
#States and values which change how Animation
#operates, but aren't absolutely vital.

	def __init__(self):
		self.full_reset()

	def full_reset(self):
	#Reset when the animation ends.

		#Config
		self.bounce_speed_cut = 2
		self.bounce_vel_cut = 1.5
		#
		self.loop_reset()

	def loop_reset(self):
		#Public Only
		self.bounced = False

#####

texture = MyTexture("assets/characters/nut/sheet.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 100,100


sprite.animation_x.target = 300
sprite.animation_x.vel = 0.5
sprite.animation_x.speed = 0.1
sprite.animation_x.bounce = True

#

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed(): pass
	key.reset_all()

	#Video
	sprite.animation_x.play()
	sprite.animation_y.play()
	
	window.clear(sf.Color(255,200,200))
	sprite.draw()
	window.view = Camera
	window.display()