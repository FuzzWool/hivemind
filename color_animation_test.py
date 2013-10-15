from code.pysfml_game import quit, window, key, sf
#########################################################
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

#####
#Create an ANIMATION class for MYSPRITE.
from code.pysfml_game import MyTexture, MySprite
from code.pysfml_game import physics_animation


class TestSprite(MySprite):
	def __init__(self, args):
		MySprite.__init__(self, args)

		self.animation_test = animation(self)


class animation:
#Contains everything which may be animated.
	
	def __init__ (self, MySprite):
		self._ = MySprite

		#Position
		self.x = physics_animation()
		self.y = physics_animation()

		#Colors
		self.red = physics_animation()
		self.green = physics_animation()
		self.blue = physics_animation()
		self.alpha = physics_animation()


	def play(self):
	#Play all animations.

		#Colors
		r,g,b,a = self._.color
		r += self.alpha.play(r)
		g += self.alpha.play(g)
		b += self.alpha.play(b)
		a += self.alpha.play(a)

		#don't go out of bounds
		def no_oob(color):
			if color < 0: color = 0
			if color > 255: color = 255
			return color
		r=no_oob(r); g=no_oob(g); b=no_oob(g); a=no_oob(a)

		self._.color = sf.Color(r,g,b,a)

#####

texture = MyTexture("assets/characters/nut/cbox.png")
sprite = TestSprite(texture)
sprite.clip.set(40,40)
sprite.position = 200,200

def animate():
	sprite.animation_test.alpha.speed = +1

sprite.color = sf.Color(255,255,255,0)
animate()

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed(): pass
	key.reset_all()

	sprite.animation_test.play()

	#Video
	window.clear(sf.Color(0,0,0))
	sprite.draw()
	window.view = Camera
	window.display()