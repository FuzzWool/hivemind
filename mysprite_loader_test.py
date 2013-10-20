import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0


####
from code.pysfml_game import MySprite_Loader

####

class tile_sprite(MySprite_Loader):
	
	def load(self, args=None):
		texture = \
		MyTexture("assets/levels/shared/level1.png")
		sprite = MySprite(texture)
		sprite.clip.set(25, 25)
		sprite.clip.use(0, 0)
		sprite.goto = 25, 25
		self.sprite = sprite


sprite_l = tile_sprite()


#########################################################

running = True
while running:
	#Logic
	if quit(): running = False

	amt = 1
	if key.A.pressed(): Camera.x -= amt
	if key.D.pressed(): Camera.x += amt
	if key.W.pressed(): Camera.y -= amt
	if key.S.pressed(): Camera.y += amt


	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite_l.draw(Camera)

	#
	window.view = Camera
	window.display()