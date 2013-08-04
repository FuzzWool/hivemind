#Testing slope collision.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

###########
from modules.pysfml_game import Dot, Line


class WIPMySprite(MySprite):
	#Axis-aligned collision checking for triangles.
	def __init__(self, args):
		MySprite.__init__(self, args)
		self.axis_collision = AxisCollision(self)

class AxisCollision:
#Collision detection designed for triangles.

	z1, z2 = 0, 0

	class axis:
	#Each axis object.
		def __init__(self, name=None): self.name = name

		point = (0,0)
		angle = 0
		length = 0


	def __init__ (self, MySprite):
		self._ = MySprite

	def calculate_angles(self, Triangle, points=None):
	#Determine the points and angle to be checked against.
	#Calculate everything for the projection.
		t = Triangle
		that = t.axis_collision

		ax = self.axis
		that.a, that.b, that.c = ax("a"), ax("b"), ax("c")

		#The main coordinates.
		if points == None:
			that.a.point = (t.x1, t.y2)
			that.b.point = (t.x2, t.y2)
			that.c.point = (t.x2, t.y1)
		else:
			that.a.point, that.b.point, that.c.point \
			= points

		#The main lengths. (Opposite the coords/angles)
		from math import hypot
		that.a.length = abs(that.a.point[1] - that.b.point[1])
		that.c.length = abs(that.c.point[0] - that.b.point[0])
		that.b.length = hypot(that.a.length, that.c.length)

		# #The main angles.
		a, b, c = \
		that.a.length, that.b.length, that.c.length

		def cos_rule(a, b, c):
		#Three lengths gets an angle.
			from math import acos, degrees
			cos1 = (b**2 + c**2 - a**2)/(2*b*c)
			return degrees(acos(cos1))

		that.b.angle = 90
		that.a.angle = cos_rule(a, b, c)
		that.c.angle = cos_rule(c, a, b)

		# self.say_lengths(that)
		# print
		# self.say_angles(that)


#	PUSHBACK (borrowed from default collision)

	def z_overlap(self, z1, z2):
		if self.z1 <= z1 <= self.z2\
		or self.z1 <= z2 <= self.z1\
		or z1 <= self.z1 <= z2\
		or z1 <= self.z2 <= z2:
			return True
		return False

	def pushback(self, Triangle):
		x1, y1, x2, y2 = Triangle.points
		that = Triangle.axis_collision
		z1, z2 = that.z1, that.z2

		AABB = self._.collision
		is_x = AABB.x_overlap(x1, x2)
		is_y = AABB.y_overlap(y1, y2)
		is_z = self.z_overlap(z1, z2)

		if is_x and is_y and is_z:
			ox = AABB.x_pushback(x1, x2)
			oy = AABB.y_pushback(y1, y2)
			oz = self.z_pushback(z1, z2)

			# print "ox", ox, "oy", oy, "oz", oz
			smallest = abs(ox); use = ox
			if abs(oy) <= smallest:
				smallest = abs(oy); use = oy
			if abs(oz) <= smallest:
				smallest = abs(oz); use = oz
			# #
			if smallest == abs(ox): self._.move(use, 0)
			else: self._.move(0, use)

	def z_pushback(self, z1, z2):
		a = self
		p = []
		if z1 <= a.z1 <= z2: p.append(z2 - a.z1)
		if z1 <= a.z2 <= z2: p.append(z1 - a.z2)
		if a.z1 <= z1 <= a.z2: p.append(a.z1 - z2)
		if a.z1 <= z2 <= a.z2: p.append(a.z2 - z1)

		lowest = None
		for i in p:
			if lowest == None: lowest = i
			if abs(i) <= lowest: lowest = i
		return lowest


#	DEBUGGING

	def say_lengths(self, that):
		t = that
		a, b, c = t.a.length, t.b.length, t.c.length
		print "a:",a," b:",b," c:",c

	def say_angles(self, that):
		a, b, c = that.a.angle, that.b.angle, that.c.angle
		print "a:",a," b:",b," c:",c
		print "Total: ", a+b+c


#	VISUAL DEBUGGING

	#Continous
	dots = []
	def make_dots(self, Triangle):
	#Make dots for each point.
		that = Triangle.axis_collision
		a = Dot(); a.center = that.a.point
		a.color = sf.Color.RED
		b = Dot(); b.center = that.b.point
		b.color = sf.Color.GREEN
		c = Dot(); c.center = that.c.point
		c.color = sf.Color.BLUE
		self.dots = [a, b, c]


	#Continous
	def make_lines(self, Triangle):
	#Make the lines connecting to the z-height,
	#to represent the collidable angle.
		t = Triangle
		that = t.axis_collision
		r = self._


		def sine_rule(a1, a2, l2):
		#Get the length.
			from math import sin, radians
			a1 = radians(a1); a2 = radians(a2)
			return (l2/sin(a2))*sin(a1)


		# PICK THE AXIS
		
		#Pick the first and second points manually.
		h = that.b.point
		no1, no2 = None, None
		if h == (t.x2, t.y2): no1 = that.c; no2 = that.b
		if h == (t.x1, t.y2): no1 = that.c; no2 = that.b
		if h == (t.x2, t.y1): no1 = that.b; no2 = that.a
		if h == (t.x1, t.y1): no1 = that.b; no2 = that.a
		
		#X is always in a direction which takes Y up.
		if that.b.point == (t.x2, t.y2)\
		or that.b.point == (t.x1, t.y1):
			x = t.x2 + r.w + 30
		if that.b.point == (t.x1, t.y2)\
		or that.b.point == (t.x2, t.y1):
			x = t.x1 - r.w - 30

		# ATTACH THE POINTS

		line_color = sf.Color.GREEN
		gap_color = sf.Color.BLACK
		
		#Triangle

		#Work out y from arbitary x.
		#Attach the first point to
		x1, y1 = no1.point
		x2 = x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		that.line1 = Line(x1, y1, x2, y2, 3, line_color)
		that.z1 = y2
		
		x1, y1 = no2.point
		x2 = x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		that.line2 = Line(x1, y1, x2, y2, 3, line_color)
		that.z2 = y2

		that.line_gap = \
		Line(x, that.z1, x, that.z2, 5, gap_color)

		#Rectangle
		line_color = sf.Color.BLUE

		#The point order
		no1 = r.x1, r.y1
		no2 = r.x2, r.y2
		if r.x2 > x:
			no1 = r.x2, r.y1
			no2 = r.x1, r.y2

		#The lines
		x1, y1 = no1
		x2 = x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		self.line1 = Line(x1, y1, x2, y2, 3, line_color)
		self.z1 = y2

		x1, y1 = no2
		x2 = x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)		
		y2 = y1 - abs(_y2)
		self.line2 = Line(x1, y1, x2, y2, 3, line_color)
		self.z2 = y2

		self.line_gap = \
		Line(x, self.z1, x, self.z2, 5, gap_color)

	def draw(self, Triangle):
		self.make_lines(Triangle)
		#
		that = Triangle.axis_collision
		that.line1.draw()
		that.line2.draw()
		that.line_gap.draw()
		#
		self.line1.draw()
		self.line2.draw()
		self.line_gap.draw()

		self.make_dots(Triangle)
		for dot in self.dots:
			dot.draw()
####

#Box
box_tex = MyTexture("img/characters/nobody/cbox.png")
box = WIPMySprite(box_tex)
box.goto = 25, 25

#Triangle
triangle_tex = MyTexture("img/triangle3.png")
triangle = WIPMySprite(triangle_tex)
triangle.goto = 200, 200

####DEBUGGING
hypo = "rd"

t = triangle
if hypo == "rd":
	\
					  a = (t.x2, t.y1)
	c = (t.x1, t.y2); b = (t.x2, t.y2);

if hypo == "ld":
	a = (t.x1, t.y1)
	b = (t.x1, t.y2); c = (t.x2, t.y2)
	triangle.clip.flip_horizontal()

if hypo == "ru":
	c = (t.x1, t.y1); b = (t.x2, t.y1);\
					  a = (t.x2, t.y2)
	triangle.clip.flip_vertical()

if hypo == "lu":
	b = (t.x1, t.y1); c = (t.x2, t.y1)
	a = (t.x1, t.y2)
	triangle.clip.flip_vertical()
	triangle.clip.flip_horizontal()

points = a, b, c
box.axis_collision.calculate_angles(triangle, points)

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

	box.axis_collision.pushback(triangle)

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	triangle.draw()
	box.draw()
	box.axis_collision.draw(triangle)
	#
	window.view = Camera
	window.display()