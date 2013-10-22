import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

############

class new_MySprite:
# WIP: Contains a sprite so that it may handle (un)loading.
# WIP: All positioning and sizing properties
#are saved for loading onto the sprite.

# Given x,y; relies on .clip for w,h


	# LOADING/UNLOADING

	sprite = None

	def __init__(self, args):
		self._sprite_args

	def draw(self):
		if self.sprite:
			self.sprite.draw()


############

texture = MyTexture("assets/levels/shared/level1.png")
sprite = MySprite(texture)
# sprite.clip.set(25, 25)
# sprite.clip.use(0, 0)
# sprite.goto = 25, 25

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite.draw()

	#
	window.view = Camera
	window.display()