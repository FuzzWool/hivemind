from code.pysfml_game import quit, window, key, sf
#########################################################
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 1
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

	target = None
	speed, vel = 1,0

	def goto(self, z):
	#Define the target.
		self.target = z

	def play(self):
	#Move closer to the target.
		if self.axis == "x": position = self._.x
		if self.axis == "y": position = self._.y

		#Move towards the target.
		if position != self.target\
		and self.target != None:
			move = self.speed
			move = self._cut_off(move)

			#Speed up.
			self.speed += self.vel

			#Confirm movement.
			if self.axis == "x": self._.move((move, 0))
			if self.axis == "y": self._.move((0, move))


	#

	def _cut_off(self, move):
	#Returns move, cuts off if the target is exceeded.
		if self.axis == "x": position = self._.x
		if self.axis == "y": position = self._.y

		if 0 < move:
			if position < self.target < position + move:
				move = self.target - position

		if move < 0:
			if position + move < self.target < position:
				move = self.target - position

		return move

#####

texture = MyTexture("assets/characters/nut/sheet.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 100,100


sprite.animation_x.goto(500)
sprite.animation_x.vel = 0.1

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