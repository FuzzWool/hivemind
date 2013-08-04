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
	#Axis-aligned collision checking for triangles.
	def __init__(self, args):
		MySprite.__init__(self, args)
		self.axis_collision = AxisCollision(self)

from modules.pysfml_game import Line
class AxisCollision:
#Collision detection designed for triangles.
	def __init__ (self, MySprite): self._ = MySprite


	z1, z2 = 0, 0

	def collide_with_triangle(self, Triangle):

		#Work out where the axis may collide.
		from math import hypot
		t = Triangle
		t_hypo = hypot(t.w, t.h)

		#Work out the angle of each side.
		def get_angle(l1, l2, l3):
			from math import acos, degrees
			cos1 = (l2**2 + l3**2 - l1**2)/(2*l2*l3)
			return degrees(acos(cos1))

		w_angle = get_angle(t.h, t.w, t_hypo)
		h_angle = get_angle(t.w, t.h, t_hypo)
		####

		def get_length(a1, l2, a2):
		#Law of sines.
			from math import sin, radians
			a1 = radians(a1); a2 = radians(a2)
			return (l2/sin(a2))*sin(a1)

		#Work out the triangle size based on an abs x.
		x = t.x2 + 100 #The absolute position.
		self.x = x

		that = Triangle.axis_collision
		
		t = Triangle
		#Triangle
		tx = x - t.x1
		ty = get_length(w_angle, tx, h_angle)
		that.z1 = t.y2 - ty

		tx = x - t.x2
		ty = get_length(w_angle, tx, h_angle)
		that.z2 = t.y2 - ty

		b = self._
		#Square
		tx = x - b.x1
		ty = get_length(w_angle, tx, h_angle)
		self.z1 = b.y1 - ty

		tx = x - b.x2
		ty = get_length(w_angle, tx, h_angle)
		self.z2 = b.y2 - ty

		self.draw_lines(Triangle)

		#####
		# Pushback
		# collision = b.collision.is_colliding(*t.points)
		# if self.z_overlap(that):
		# 	b.collision.pushback(t)
		self.pushback(*t.points, z1=that.z1, z2=that.z2)

	def z_overlap(self, z1, z2):
		if self.z1 <= z1 <= self.z2\
		or self.z1 <= z2 <= self.z1\
		or z1 <= self.z1 <= z2\
		or z1 <= self.z2 <= z2:
			return True
		return False

#	PUSHBACK (borrowed from default collision)

	def pushback(self, x1, y1, x2, y2, z1, z2):

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


#	VISUAL DEBUG
	def draw_lines(self, Triangle):
		b = self._
		t = Triangle
		that = t.axis_collision

		if self.z_overlap(that.z1, that.z2):
			color = sf.Color.GREEN
		else:
			color = sf.Color.RED

		x = self.x
		#Triangle lines.
		tx = x - t.x1
		self.line3 = Line(t.x1, t.y2, t.x1 + tx, that.z1, 3, sf.Color.GREEN)

		tx = x - t.x2
		self.line4 = Line(t.x2, t.y2, t.x2 + tx, that.z2, 3, sf.Color.GREEN)

		self.that_gapline = \
		Line(t.x2 + tx, that.z1, t.x2 + tx, that.z2, 5, color)

		#Square lines.
		tx = x - b.x1
		self.line1 = Line(b.x1, b.y1, b.x1 + tx, self.z1, 3, sf.Color.GREEN)
		tx = x - b.x2
		self.line2 = Line(b.x2, b.y2, b.x2 + tx, self.z2, 3, sf.Color.GREEN)

		self.gapline = Line(b.x2 + tx, self.z1, b.x2 + tx, self.z2, 5, color)


	def draw(self):
		self.line3.draw()
		self.line4.draw()
		self.that_gapline.draw()

		self.line1.draw()
		self.line2.draw()
		self.gapline.draw()

####

#Box
box_tex = MyTexture("img/characters/nobody/cbox.png")
box = WIPMySprite(box_tex)
box.goto = 25, 25

#Triangle
triangle_tex = MyTexture("img/triangle2.png")
triangle = WIPMySprite(triangle_tex)
triangle.goto = 400, 350

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

	box.axis_collision.collide_with_triangle(triangle)

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	triangle.draw()
	box.draw()
	box.axis_collision.draw()
	#
	window.view = Camera
	window.display()