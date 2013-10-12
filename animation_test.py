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

		self.testanimation = TestAnimation(self)


class TestAnimation:
#Provides short-hands for calculating easy physics.

	def __init__(self, MySprite):
		self._ = MySprite
		self.A, self.B = (0,0),(0,0)
		self._reset_values()

	####

	xSpeed, ySpeed = 1, 1
	xVel, yVel = 0, 0

	def goto(self, x=0, y=0): #call once
	#Steadily move from A to B.
		self.A = self._.position
		self.B = x, y
		self._reset_values()

	#

	def play(self):
	#Continue operations.
	#Will be idle if not called every loop.

		this_x, that_x = self._.x, self.B[0]
		this_y, that_y = self._.y, self.B[1]

		#Get closer...
		x, y = 0,0
		if this_x < that_x: x = +self.xSpeed
		if this_x > that_x: x = -self.xSpeed
		if this_y < that_y: y = +self.ySpeed
		if this_y > that_y: y = -self.ySpeed

		#...but don't overshoot!
		if 0 < x:
			if this_x < that_x < this_x + x:
				x = that_x - this_x
		if x < 0:
			if this_x + x < that_x < this_x:
				x = that_x - this_x
		if 0 < y:
			if this_y < that_y < this_y + y:
				y = that_y - this_y
		if y < 0:
			if this_y < that_y < this_y + y:
				y = that_y - this_y

		#Speed up.
		self.xSpeed += self.xVel
		self.ySpeed += self.yVel

		# if (x,y) != (0,0): print x,y
		self._.move((x,y))

	####

	def _reset_values(self): #init, goto
		self.xSpeed, self.ySpeed = 1, 1
		self.xVel, self.yVel = 0, 0






#####

texture = MyTexture("assets/characters/nut/sheet.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 100,100

sprite.testanimation.goto(500,100)
sprite.testanimation.xSpeed = 0
sprite.testanimation.xVel = 0.1

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed(): pass
	key.reset_all()


	#Video
	window.clear(sf.Color(255,200,200))

	sprite.testanimation.play()
	sprite.draw()

	window.view = Camera
	window.display()