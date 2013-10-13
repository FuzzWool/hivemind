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

	#

	#Movement settings
	target = None
	speed, vel = 1,0


	def goto(self, z):
	#Define the target.
		self.target = z

	def play(self):
	#Move closer to the target.
		position = self.position()

		#Move towards the target.
		if position != self.target\
		and self.target != None:
			move = self.speed

			#SPECIAL MOVEMENT
			if self._end_passed(move):
				# move = self._cut_off()
				move = self._bounce(move)

			#Speed up.
			self.speed += self.vel

			#Confirm movement.
			if self.axis == "x": self._.move((move, 0))
			if self.axis == "y": self._.move((0, move))


	#

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

	def _cut_off(self): #play
	#Halt the sprite as soon as it reaches the target.
		return self.target - self.position()

	def _bounce(self, move): #play
	#Bounce the sprite against the 'wall' of the target.
		self.speed = -(self.speed/2)
		self.vel = abs(self.vel/1.5)

		#Stop doing this.
		frames_since = self.speed + (self.vel*10)
		if abs(self.speed) < frames_since:
			self.speed = self._cut_off()
			self.vel = 0

		move = self.speed
		return move


	# utilities

	def position(self): #play
		if self.axis == "x": return self._.x
		if self.axis == "y": return self._.y


#####

texture = MyTexture("assets/characters/nut/sheet.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 100,100


sprite.animation_x.goto(300)
sprite.animation_x.vel = 0.5
sprite.animation_x.speed = 0.1

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