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
class slope_collision:
	def __init__(self, MySprite): self._ = MySprite


	#	SETTINGS

	#Set the points defining the intersection
	a, b = 0, 0
	#Set where the right-angle should be anchored (hypot)
	anchor = "rd"
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
		is_z = self.z_overlap(Slope)

		if is_x and is_y and is_z:
			ox1 = AABB.x_pushback(x1, x2)
			oy1 = AABB.y_pushback(y1, y2)

			ox2 = -self.x_overlap_amt(Slope)
			oy2 = -self.y_overlap_amt(Slope)

			#FIND the smallest pushback.
			small = ox2
			if abs(oy2) <= abs(small): small = oy2
			if abs(ox1) <= abs(small): small = ox1
			if abs(oy1) <= abs(small): small = oy1

			#MOVE BY the smallest pushback.
			if small in [oy1, oy2]:
				# print small
				self._.move(0, small) 
			else:
				# print small
				self._.move(small, 0)



	def z_overlap(self, Slope):
	#If the slope's hypotenuse is being crossed.
		x = self.x_overlap_amt(Slope)
		y = self.y_overlap_amt(Slope)
		is_x = bool(0 <= x)
		is_y = bool(0 <= y)

		if is_x and is_y: return True
		return False

	## The amount of the hypotenuse being overlapped.
	def x_overlap_amt(self, Slope):
		ratio = Slope.w/Slope.h
		#
		distance = self._.y2 - Slope.y1
		distance *= ratio
		x_intersect = Slope.x2 - distance
		return self._.x2 - x_intersect

	def y_overlap_amt(self, Slope):
		ratio = Slope.h/Slope.w
		#
		distance = self._.x2 - Slope.x1
		distance *= ratio
		y_intersect = Slope.y2 - distance
		return self._.y2 - y_intersect
	#


	# def y_pushback(self, y1, y2):
	# 	a = self._
	# 	p = []
	# 	if y1 <= a.y1 <= y2: p.append(y2 - a.y1)
	# 	if y1 <= a.y2 <= y2: p.append(y1 - a.y2)
	# 	if a.y1 <= y1 <= a.y2: p.append(a.y1 - y2)
	# 	if a.y1 <= y2 <= a.y2: p.append(a.y2 - y1)

	# 	lowest = None
	# 	for i in p:
	# 		if lowest == None: lowest = i
	# 		if abs(i) <= lowest: lowest = i
	# 	return lowest


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
triangle_tex = MyTexture("img/triangle2.png")
triangle = WIPMySprite(triangle_tex)
triangle.goto = 200, 150
#####

hypo = "ld"

t = triangle
if hypo == "rd":
	\
					  a = (t.x2, t.y1)
	c = (t.x1, t.y2)

if hypo == "ld":
	\
	a = (t.x1, t.y1);\
					 c = (t.x2, t.y2)
	triangle.clip.flip_horizontal()

if hypo == "ru":
	\
	c = (t.x1, t.y1);\
					  a = (t.x2, t.y2)
	triangle.clip.flip_vertical()

if hypo == "lu":
	\
					 c = (t.x2, t.y1)
	a = (t.x1, t.y2)
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