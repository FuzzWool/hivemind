class physics_animation(object):
#Provides short-hands for calculating easy physics.
#One for each axis: x and y.
	def __init__(self, called_directly=True):

		#Pre-sets - they subclass this class.
		if called_directly:
			self.bounce = bounce(False)
			self.oscillate = oscillate(False)


	#Public

	end = None
	speed, vel = 0, 0

	def play(self, point): #float
	#Performs movement operations,
	#returns the amount to be moved by.

		if self._just_passed_end(point, self.speed):
			self.just_passed_end_event(point)

		move = self.speed
		self.speed += self.vel
		return move



	# Overridables

	def just_passed_end_event(self, point): #void
		self.cut_off(point)

	def cut_off(self, point): #void
		self.speed = self.end - point
		self.vel = 0


	# Private

	def _just_passed_end(self, point, move): #bool
		if point <= self.end <= point+move: return True
		if point >= self.end >= point+move: return True
		return False

	#

class bounce(physics_animation):
#Bounce when the end has been reached.

	vel_divide = 1
	speed_divide = 1

	def just_passed_end_event(self, point):

		#Bounce back.
		self.speed = \
		-(self.speed-self.vel/self.speed_divide)
		self.vel = self.vel/self.vel_divide

		#Stopping when vel divides.
		if abs(self.speed) < 0.1:
			self.cut_off(point)

		#Stopping when vel multiplies.
		if abs(self.vel) > abs(self.speed):
			self.cut_off(point)


		#Ended.
		if self.vel == 0: self.cut_off(point)



class oscillate(physics_animation):
#When the end is passed, it gradually changes direction.
	
	vel_divide = 1

	def just_passed_end_event(self, point):
		self.vel = -(self.vel/self.vel_divide)

		#Stopping
		if abs(self.vel) > abs(self.speed):
			self.cut_off(point)
		if self.vel == 0: self.cut_off(point)