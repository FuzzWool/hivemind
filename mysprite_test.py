
import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

###
# GOAL: MySprite plays nice with GameRectangle.
from code.pysfml_game import GameRectangle


class TestSprite(sf.Sprite, GameRectangle):


	#Linking INHERITANCE
	@property
	def x(self): return self.position[0]
	@x.setter
	def x(self, x): self.position = x, self.y

	@property
	def y(self): return self.position[1]
	@y.setter
	def y(self, y): self.position = self.x, y

	@property
	def w(self): return self.texture.size[0]
	@property
	def h(self): return self.texture.size[1]
	#

	def draw(self): window.draw(self)


###



Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

texture = MyTexture("assets/levels/shared/level1.png")
sprite = MySprite(texture)


sprite.position = 300,300

# sprite.clip.set(25, 25)
# sprite.clip.use(0, 0)
# sprite.goto = 25, 25

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		sprite.position = 0,0

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite.draw()

	#
	window.view = Camera
	window.display()