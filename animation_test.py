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


class TestAnimation(object):
#Provides short-hands for calculating easy physics.
#One for each axis: x and y.

	def __init__(self, MySprite, axis):
		self._ = MySprite
		self.axis = axis
		self.config = config(self)


	# PUBLIC

	#Values	
	target = None
	speed, vel = 1,0


	#States - (@property details in private)

	#stopped when
	stop_when_positive = True
	stop_when_negative = True

	#when stopped
	cut_off = True
	bounce = False


	#Method
	def play(self):
	#Move closer to the target.
		self.config.loop_reset()
		position = self.position

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
		position = self.position

		if 0 < move and self.stop_when_positive:
			if position <= self.target <= position + move:
				return True

		if move < 0 and self.stop_when_negative:
			if position + move <= self.target <= position:
				return True

		return False

	def f_cut_off(self): #play
	#Halt the sprite as soon as it reaches the target.
		return self.target - self.position

	def m_bounce(self, move): #play
	#Bounce the sprite against the 'wall' of the target.
		self.config.bounced = True
		speed_cut = self.config.bounce_speed_cut
		vel_cut = self.config.bounce_vel_cut

		#Bounce back.
		self.speed = -(self.speed/speed_cut)
		self.vel = (self.vel/vel_cut)

		#Stop doing this.
		frames_since = self.speed + (self.vel*10)
		if abs(self.speed) < abs(frames_since):
			self.speed = self.f_cut_off()
			self.vel = 0

		self.speed += self.vel
		move = self.speed

		print self.speed, self.vel, move

		return move


	# utilities

	def reset(self): #play
	#A complete reset of every single value.
		
		#Values
		self.target = None
		self.speed, self.vel = 1,0
		#
		self.stop_when_positive = True
		self.stop_when_negative = True
		self._reset_states()
		#
		self.config.full_reset()

	@property
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
		if self.position == self.target\
		or self.target == None:
			if (self.speed<0 and self.stop_when_negative)\
			or (0<self.speed and self.stop_when_positive):
				return True
		return False


class config(object):
#States and values which change how Animation
#operates, but aren't absolutely vital.

	def __init__(self, Animation):
		self._ = Animation
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


	#SHORT-HANDS

	@property
	def bounce_infinitely(self):
		if self.bounce_speed_cut == 1\
		and self.bounce_vel_cut == 1:
			return True
		return False
	@bounce_infinitely.setter
	def bounce_infinitely(self, truth):
		if truth:
			self._.bounce = True
			self.bounce_speed_cut = 1
			self.bounce_vel_cut = 1
		else: pass


#####

texture = MyTexture("assets/characters/nut/cbox.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 200,200


def animate():
	sprite.animation_x.target = sprite.x
	sprite.animation_x.vel = float(-0.1)
	sprite.animation_x.speed = float(1)
	sprite.animation_x.stop_when_positive = False
	sprite.animation_x.config.bounce_infinitely = True
#

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		if sprite.animation_x.stopped:
			animate()

		else:
			sprite.animation_x.cut_off = True


	key.reset_all()

	#Video
	sprite.animation_x.play()
	# sprite.animation_y.play()
	
	window.clear(sf.Color(0,0,0))
	sprite.draw()
	window.view = Camera
	window.display()