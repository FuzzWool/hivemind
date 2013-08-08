#Testing slope collision.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0
###########
class WIPMySprite(MySprite):
	
	def __init__(self, args):
		MySprite.__init__(self, args)
		self.slope_collision = slope_collision(self)


from modules.pysfml_game import Dot
class slope_collision(object):
	def __init__(self, MySprite):
		self._ = MySprite

		#Set the points defining the intersection
		self.a, self.b = 0, 0
		#Set where the right-angle should be anchored
		self.anchor = "rd"

	@property
	def anchor_x(self): return self.anchor[0]
	@property
	def anchor_y(self): return self.anchor[1]

	#	COLLISION

	def pushback(self, Slope):
	#Against a slope with it's A and B set.
	#Borrows from MySprite.collision
		x1, y1, x2, y2 = Slope.points
		AABB = self._.collision

		is_x = AABB.x_overlap(x1, x2)
		is_y = AABB.y_overlap(y1, y2)
		is_z = self.is_z(Slope)


		if is_x and is_y and is_z:
			ox1 = AABB.x_pushback(x1, x2)
			oy1 = AABB.y_pushback(y1, y2)

			#The slope's pushback's positivity depends
			#on anchor.
			that = Slope.slope_collision
			if that.anchor in ["rd", "ld"]:
				oy2 = -self.y_overlap_amt(Slope)
			if that.anchor in ["ru", "lu"]:
				oy2 = self.y_overlap_amt(Slope)

			#FIND the smallest pushback.
			# small = ox2
			small = oy2
			if abs(oy2) <= abs(small): small = oy2
			if abs(ox1) <= abs(small): small = ox1
			if abs(oy1) <= abs(small): small = oy1

			#MOVE BY the smallest pushback.
			if small in [oy1, oy2]:
				self._.move(0, small) 
			else:
				self._.move(small, 0)

	def is_z(self, Slope):
		z = self.y_overlap_amt(Slope)
		return bool(0 < z)

	def y_overlap_amt(self, Slope):
	#Returns a positive value.
		that = Slope.slope_collision

		#Gradient
		w = that.b[0] - that.a[0]; w = abs(w)
		h = that.b[1] - that.a[1]; h = abs(h)
		ratio = h/w

		#X from origin
		y_lowering = self._.x2 - that.a[0]
		y_lowering *= ratio

		if that.anchor == "rd":
			if h <= y_lowering: y_lowering = h
			gap = self._.y2 - that.a[1]
			return +(gap + y_lowering)

		if that.anchor == "ru":
			if 0 <= y_lowering: y_lowering = 0
			gap = self._.y1 - that.a[1]
			return -(gap - y_lowering)


		y_lowering = self._.x1 - Slope.x1
		y_lowering *= ratio

		if that.anchor == "ld":
			if y_lowering <= 0: y_lowering = 0
			gap = self._.y2 - that.a[1]
			return +(gap - y_lowering)

		if that.anchor == "lu":
			if y_lowering <= 0: y_lowering = 0
			gap = self._.y1 - that.a[1]
			return -(gap + y_lowering)
	#


	# VISUAL DEBUG

	adot, bdot = None, None
	def draw(self):
		#Make the dots.
		if (self.adot, self.bdot) == (None, None):
			self.adot = Dot(); self.adot.goto = self.a
			self.bdot = Dot(); self.bdot.goto = self.b
		#Draw the dots.
		self.adot.draw(); self.bdot.draw()


###########

#Box
box_tex = MyTexture("img/characters/nobody/cbox.png")
box = WIPMySprite(box_tex)
box.goto = 25, 25

#TRIANGLE
triangle_tex = MyTexture("img/triangle1.png")
triangle = WIPMySprite(triangle_tex)
triangle.goto = 200, 200
#####

hypo = "rd"

t = triangle
if hypo == "rd":
	\
					  c = (t.x2, t.y1+25)
	a = (t.x1, t.y2-25)

if hypo == "ru":
	\
	c = (t.x1, t.y1-25);\
					  a = (t.x2, t.y2+25)
	triangle.clip.flip_vertical()

if hypo == "ld":
	\
	a = (t.x1, t.y1+25);\
					 c = (t.x2, t.y2-25)
	triangle.clip.flip_horizontal()

if hypo == "lu":
	\
					 c = (t.x2, t.y1+25)
	a = (t.x1, t.y2-25)
	triangle.clip.flip_vertical()
	triangle.clip.flip_horizontal()

triangle.slope_collision.a = a
triangle.slope_collision.b = c
triangle.slope_collision.anchor = hypo
print triangle.slope_collision.anchor
#########################################################
running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	amt = 5
	if key.A.held(): box.move(-amt, 0)
	if key.D.held(): box.move(+amt, 0)
	if key.W.held(): box.move(0, -amt)
	if key.S.held(): box.move(0, +amt)

	box.slope_collision.pushback(triangle)

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#
	triangle.draw()
	box.draw()
	triangle.slope_collision.draw()
	#
	window.view = Camera
	window.display()