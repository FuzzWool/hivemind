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

	x = 0
	w_angle, h_angle = None, None #The actual angles.
	z1, z2 = None, None #The height of the angle.

	def collide_with_triangle(self, Triangle):
	#Check whether or not the rect is colliding with
	#a triangle.

		#Calculate the angle for the triangle and itself,
		#if needed.
		self.calculate_angles(Triangle)

		#Check for an overlap.
		that = Triangle.axis_collision
		if self.z1 < that.z1 < self.z2\
		or that.z1 < self.z1 < that.z2\
		or self.z1 < that.z2 < self.z2\
		or that.z1 < self.z2 < that.z2:
			print "collision"

		#Debugging.
		self.make_lines\
		(Triangle, self.w_angle, self.h_angle)



	def calculate_angles(self, Triangle):
	#Calculate the angle needed for collision detection,
	#for both itself and the Triangle.
		a = self._
		b = Triangle
		that = b.axis_collision
		x = self.x

		from math import hypot
		hypo = hypot(b.w, b.h)

		def get_angle(l1, l2, l3):
		#Law of cosines.
			from math import acos, degrees
			cos1 = (l2**2 + l3**2 - l1**2)/(2*l2*l3)
			return degrees(acos(cos1))

		w_angle = get_angle(b.w, b.h, hypo)
		h_angle = get_angle(b.h, b.w, hypo)

		#Get a values for checking collisions.
		ay = self.get_length(w_angle, x - a.x2, h_angle)
		by = self.get_length(w_angle, x - b.x2, h_angle)

		#Apply calculations
		self.w_angle, self.h_angle = w_angle, h_angle
		self.z1 = a.y1 - ay
		self.z2 = self.z1 + a.h
		that.z1 = b.y1 - by
		that.z2 = that.z1 + b.h


	def get_length(self, a1, l2, a2):
	#Law of sines.
		from math import sin
		return (l2/sin(a2))*sin(a1)


	#	DEBUGGING

	def make_lines(self, Triangle, w_angle, h_angle):
		#Draw the lines.
		#Get the length individually.
		self.x = Triangle.x2 + Triangle.w
		x = self.x

		# #Box lines
		a = self._
		ay = self.get_length(w_angle, x-a.x2, h_angle)
		self.line3 = Line(a.x1, a.y2, x, a.y1-ay,2)
		self.line4 = Line(a.x2, a.y2, x, a.y2-ay,2)
		
		#Triangle lines
		b = Triangle
		by = self.get_length(w_angle, x-b.x2, h_angle)
		self.line1 = Line(b.x2, b.y1, x, b.y1-by, 2)
		self.line2 = Line(b.x2, b.y2, x, b.y2-by, 2)

		#Total gap
		self.total_gap_line = \
		Line(x+20, b.y1-by, x+20, a.y2-ay,\
			5, sf.Color.RED)

		#a length for self
		b = self._
		by = self.get_length(w_angle, x-b.x2, h_angle)
		self.b_gap = Line(x, b.y1-by, x, b.y2-by,\
						10, sf.Color.BLUE)

		#a length for triangle
		t = Triangle
		ty = self.get_length(w_angle, x-t.x2, h_angle)
		self.t_gap = Line(x, t.y1-ty, x, t.y2-ty,\
						5, sf.Color.GREEN)

	def draw(self):
		self.line1.draw()
		self.line2.draw()
		#
		self.line3.draw()
		self.line4.draw()
		#
		self.total_gap_line.draw()
		self.b_gap.draw()
		self.t_gap.draw()
####

#Box
box_tex = MyTexture("img/characters/nobody/cbox.png")
box = WIPMySprite(box_tex)
box.goto = 25, 25

#Triangle
triangle_tex = MyTexture("img/triangle2.png")
triangle = WIPMySprite(triangle_tex)
triangle.goto = 400, 200

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