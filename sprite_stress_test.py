import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

class Foo:
	def __init__(self):
		pass
		# self.f1 = _foo(self)
		# self.f2 = _foo(self)
		# self.f3 = _foo(self)
		# self.f4 = _foo(self)
		# self.f5 = _foo(self)
		# self.f6 = _foo(self)
		# self.f7 = _foo(self)
		# self.f8 = _foo(self)
		# self.f9 = _foo(self)
		# self.f10 = _foo(self)
		# self.f11 = _foo(self)
		# self.f12 = _foo(self)
		# self.f13 = _foo(self)
		# self.f14 = _foo(self)
		# self.f15 = _foo(self)

	def draw(self):
		pass

# class _foo:
# 	def __init__(self, Foo):
# 		self._ = Foo

# 		self.a1 = 0
# 		self.a2 = 1
# 		self.a3 = 2
# 		self.a4 = 3
# 		self.a5 = 4
# 		self.a6 = 5
# 		self.a7 = 6
# 		self.a8 = 7
# 		self.a9 = 8
# 		self.a10 = 9

# 	def f1(self): pass
# 	def f2(self): pass

# sprites = []
texture = MyTexture("assets/levels/shared/level1.png")
# for x in range(500):
# 	sprites.append([])
# 	for y in range(100):
# 		# f = Foo()
# 		# sprites[x].append(f)
# 		sprite = MySprite(texture)
# 		sprite.clip.set(25, 25)
# 		sprite.clip.use(0, 0)
# 		sprite.position = x*25, y*25
# 		sprites[x].append(sprite)

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

	# for x in sprites:
	# 	for y in x:
	# 		y.draw()

	#
	window.view = Camera
	window.display()