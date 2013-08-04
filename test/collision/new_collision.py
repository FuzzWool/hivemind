#Test collisions for individual sides.

#####WIP
from modules.pysfml_game import MySprite
class WIPMySprite(MySprite):
	def __init__(self, args):
		MySprite.__init__(self, args)
		self.collision = collision(self)


class collision:
#Handles basic AABB collision checking.
#Checks X and Y individually.

	def __init__(self, MySprite): self._ = MySprite 

	def __call__ (self, x1=0, y1=0, x2=0, y2=0,\
				  MySprite=None):
		#Use another MySprite if possible.
		#Use coordinates or a Sprite!
		if  not type(x1) == int \
		and not type(x1) == float:
			MySprite = x1

		if MySprite != None:
			x1, y1, x2, y2 = MySprite.points
		return self.is_colliding(x1, y1, x2, y2)
	#
	def is_colliding(self, x1, y1, x2, y2):
		is_x = self.x_overlap(x1, x2)
		is_y = self.y_overlap(y1, y2)

		if is_x and is_y: return True
		else: return False


	def pushback(self, x1=0, y1=0, x2=0, y2=0,\
				MySprite=None):
		#Use another MySprite if possible.
		#Use coordinates or a Sprite!
		if  not type(x1) == int \
		and not type(x1) == float:
			MySprite = x1

		if MySprite != None:
			x1, y1, x2, y2 = MySprite.points
		return self._pushback(x1, y1, x2, y2)
	#
	def _pushback(self, x1, y1, x2, y2):
		is_x = self.x_overlap(x1, x2)
		is_y = self.y_overlap(y1, y2)

		if is_x and is_y:
			ox = self.x_pushback(x1, x2)
			oy = self.y_pushback(y1, y2)

			if abs(ox) <= abs(oy): self._.move(ox, 0)
			else:				  self._.move(0, oy)

	#

	#Simply detects if there is any overlapping.
	def x_overlap(self, x1, x2):
		a = self._
		if x1 <= a.x1 <= x2: return True
		if x1 <= a.x2 <= x2: return True
		if a.x1 <= x1 <= a.x2: return True
		if a.x1 <= x2 <= a.x2: return True
		return False

	def y_overlap(self, y1, y2):
		a = self._
		if y1 <= a.y1 <= y2: return True
		if y1 <= a.y2 <= y2: return True
		if a.y1 <= y1 <= a.y2: return True
		if a.y1 <= y2 <= a.y2: return True
		return False
	#

	#Works out the shortest pushback.
	def x_pushback(self, x1, x2):
		a = self._
		p = []
		if x1 <= a.x1 <= x2: p.append(x2 - a.x1)
		if x1 <= a.x2 <= x2: p.append(x1 - a.x2)
		if a.x1 <= x1 <= a.x2: p.append(a.x1 - x2)
		if a.x1 <= x2 <= a.x2: p.append(a.x2 - x1)

		lowest = None
		for i in p:
			if lowest == None: lowest = i
			if abs(i) <= lowest: lowest = i
		return lowest

	def y_pushback(self, y1, y2):
		a = self._
		p = []
		if y1 <= a.y1 <= y2: p.append(y2 - a.y1)
		if y1 <= a.y2 <= y2: p.append(y1 - a.y2)
		if a.y1 <= y1 <= a.y2: p.append(a.y1 - y2)
		if a.y1 <= y2 <= a.y2: p.append(a.y2 - y1)

		lowest = None
		for i in p:
			if lowest == None: lowest = i
			if abs(i) <= lowest: lowest = i
		return lowest


#####	Extra checks
#For resetting jumps, etc.

	#Side checks.
	def bottom_to_top(self, x1, y1, x2, y2):
	#If a's bottom is colliding with b's top.
		if self._x_collision(x1, x2):
			a = self._
			if a.y2 == y1: return True
		return False

	def top_to_bottom(self, x1, y1, x2, y2):
		if self._x_collision(x1, x2):
			a = self._
			if a.y1 == y2: return True
		return False

	def left_to_right(self, x1, y1, x2, y2):
		if self._y_collision(y1, y2):
			a = self._
			if a.x1 == x2: return True
		return False

	def right_to_left(self, x1, y1, x2, y2):
		if self._y_collision(y1, y2):
			a = self._
			if a.x2 == x1: return True
		return False
	#


	#Simply detects if there is any collision (no overlap)
	def _x_collision(self, x1, x2):
		a = self._
		if x1 < a.x1 < x2: return True
		if x1 < a.x2 < x2: return True
		if a.x1 < x1 < a.x2: return True
		if a.x1 < x2 < a.x2: return True
		return False

	def _y_collision(self, y1, y2):
		a = self._
		if y1 < a.y1 < y2: return True
		if y1 < a.y2 < y2: return True
		if a.y1 < y1 < a.y2: return True
		if a.y1 < y2 < a.y2: return True
		return False

####

######



import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

texture = MyTexture("img/characters/nobody/cbox.png")
A = WIPMySprite(texture)
A.goto = 25, 25

texture2 = MyTexture("img/characters/nobody2/cbox.png")
B = WIPMySprite(texture2)
B.goto = 500, 200

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#Controls
	amt = 5
	if key.W.held(): A.move(0, -amt)
	if key.S.held(): A.move(0, +amt)
	if key.A.held(): A.move(-amt, 0)
	if key.D.held(): A.move(+amt, 0)
	#

	A.collision.pushback(B)

	#Video
	window.clear(sf.Color.WHITE)
	#
	A.draw()
	B.draw()
	#
	window.view = Camera
	window.display()