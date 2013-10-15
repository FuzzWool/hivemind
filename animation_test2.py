from code.pysfml_game import quit, window, key, sf
#########################################################
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

#####
#Create an ANIMATION class for MYSPRITE.
from code.pysfml_game import MyTexture, MySprite
from code.pysfml_game import physics_animation


class TestSprite(MySprite):
	def __init__ (self, args):
		MySprite.__init__(self, args)

		self.animation_x = physics_animation()
		self.animation_y = physics_animation()


#####

texture = MyTexture("assets/characters/nut/cbox.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 200,200


def animate():
	sprite.animation_x.oscillate.speed = 1
	sprite.animation_x.oscillate.vel = 0.1
	sprite.animation_x.oscillate.end = sprite.x+0.1

	sprite.animation_x.oscillate.vel_divide = 1

animate()

#

running = True
while running:
	#Logic

	if quit(): running = False
	if key.RETURN.pressed():
		pass

	key.reset_all()

	#Video
	sprite.x += sprite.animation_x.oscillate.play(sprite.x)
	
	window.clear(sf.Color(0,0,0))
	sprite.draw()
	window.view = Camera
	window.display()