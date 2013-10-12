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


	def play(self): #loop
	#Continue operations.
	#Will be idle if not called every loop.

		#move
		x, y = 0, 0
		if self._.x < self.B[0]: x = +1
		if self._.x > self.B[0]: x = -1
		if self._.y < self.B[1]: y = +1
		if self._.y > self.B[1]: y = -1

		self._.move((x,y))

	####

	def goto(self, x=None, y=None): #call once
	#Steadily move from A to B.
		self.A = self._.position




#####

texture = MyTexture("assets/characters/nut/sheet.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 100,100

sprite.testanimation.goto(200,200)

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