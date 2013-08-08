from window import sf, window
from geometry import Rectangle

texture = sf.Texture.load_from_file
MyTexture = sf.Texture.load_from_file

class MySprite(sf.Sprite, Rectangle):
#Provides additional functionality for sf.Sprite.
	def __init__ (self, arg):
		sf.Sprite.__init__(self, arg)
		
		#All sub-classes
		self.resize = resize(self)
		self.clip = clip(self)
		self.box = box(self)
		self.children = []; self.children_class = children_class(self)
		self.collision = collision(self)
		self.animation = animation(self)
		self.axis_collision = AxisCollision(self)

	#Positioning is handled by goto instead of position.
	#Position can't be overriden, but it needs to be for children.
	@property
	def goto(self):
		return self.position[0] - \
				(self.origin[0] * self.scale[0]),\
			   self.position[1] - \
				(self.origin[1] * self.scale[1])
	@goto.setter
	def goto(self, args):
		self.children_class.goto(args)
		args = args[0] + self.origin[0],\
			   args[1] + self.origin[1]
		self.position = args
	#

	@property
	def x(self): return self.goto[0]
	@x.setter
	def x(self, x): self.goto = x, self.y

	@property
	def y(self): return self.goto[1]
	@y.setter
	def y(self, y): self.goto = self.x, y

	@property
	def w(self): return self.global_bounds.width
	@w.setter
	def w(self, arg):
		self.children_class.w(arg)
		self.resize.w(arg, False)

	@property
	def h(self): return self.global_bounds.height
	@h.setter
	def h(self, arg):
		self.children_class.h(arg)
		self.resize.h(arg, False)

	def move(self, x=0, y=0):
		x, y = x + self.x, y + self.y
		self.goto = x, y

	def draw(self): window.draw(self)


class resize: #PRIVATE
#Scales the image proportionally based on absolute sizing.
	def __init__ (self, mysprite):
		self._ = mysprite

	def w(self, w, to_scale = True):
		if w != 0:
			rw = w / self._.w
			#
			if to_scale == False:
				rh = 1
			else:
				rh = rw
			#
			self._.scale(rw, rh)

	def h(self, h, to_scale = True):
		if h != 0:
			rh = h / self._.h
			#
			if to_scale == False:
				rw = 1
			else:
				rw = rh
			#
			self._.scale(rw, rh)


class clip:
#Set grid size, chooses grid position. For spritesheets.
	def __init__ (self, MySprite):
		self._ = MySprite
		self.ox, self.oy, self.w, self.h = 0, 0, 0, 0
		self.x, self.y = 0, 0

		self.set(self._.w, self._.h)
		self.use(0, 0)

	def __call__ (self, *args): self.set(*args)
	def set(self, w, h, x=0, y=0): #Absolute
	#Sets the grid boundaries for displaying.
		self.w, self.h, self.ox, self.oy = w, h, x, y
		self._.set_texture_rect(\
			sf.IntRect(x, y, w, h))

	def division(self, x, y): #Relative
		w, h = self._.w / x, self._.h / y
		self.set(w, h)

	def use(self, x=-1, y=-1):
	#Selects which portion of the spritesheet to display.
		if x == -1: x = self.x
		if y == -1: y = self.y

		self.x, self.y = x, y
		ox, oy, w, h = self.ox, self.oy, self.w, self.h

		if self.flipped_horizontal:x += 1; x1 = ox+(w*-x)
		else: x1 = ox+(w*x)
		if self.flipped_vertical: y += 1; y1 = oy+(h*-y)
		else: y1 = oy+(h*y)
		
		x2, y2 = w, h
		self._.set_texture_rect(sf.IntRect(x1,y1,x2,y2))


	#	FLIPPING

	flipped_vertical = False
	flipped_horizontal = False
	@property
	def flipped(self): return self.flipped_horizontal

	#

	def flip(self):
		self.flip_horizontal()

	def flip_horizontal(self):
		self.flipped_horizontal \
		= not self.flipped_horizontal
		self.w = -self.w
		self.set(self.w, self.h)
		self.use(self.x, self.y)

	def flip_vertical(self):
		self.flipped_vertical \
		= not self.flipped_vertical
		self.h = -self.h
		self.set(self.w, self.h)
		self.use(self.x, self.y)



class children_class: #PRIVATE
#Sprites which are associated with the movements and actions of our parent sprite.
	def __init__ (self, mysprite): self._ = mysprite

	def goto(self, args):
	#The distance moved by the parent is calculated and given to the children.
		x, y = args[0] - self._.x, args[1] - self._.y
		for s in self._.children:
			s.move(x, y)

	#Works out the proportion of the parent's scale. Applies to children.
	def w(self, arg):
		proportion = arg / self._.w
		for s in self._.children:
			s.w = proportion * s.w

	def h(self, arg):
		p = arg / self._.h
		for s in self._.children:
			s.h = p * s.h
	#

class box(Rectangle):
#Handles the sprite's proportional positioning.
	def __init__ (self, mysprite):
		self._ = mysprite
		self.rect = None

	#Box me! Centers the sprite within the box.
	def me(self):
		self._.center = self.center

	#Centers sprite, and children, within a row/column.
	def center_row(self, sprites=None):
		if sprites == None:
			sprites = []; sprites.append(self._)
			for s in self._.children: sprites.append(s)

		slab = self.w / float((len(sprites)+1))
		i = 1
		for s in sprites:
			s.center = self.x + (slab * i), self.center[1]
			i += 1

	def center_column(self, sprites=None):
		if sprites == None:
			sprites = []; sprites.append(self._)
			for s in self._.children: sprites.append(s)

		slab = self.h / float((len(sprites)+1))
		i = 1
		for s in sprites:
			s.center = self.center[0], self.y + (slab * i)
			i += 1
	#

	def draw(self):
	#Draws a box for the sake of debugging.
	#Drawn again every time there's a change.
		def make_rect():
			self.rect = sf.RectangleShape((self.w, self.h))
			self.rect.position = self.x, self.y
			self.rect.fill_color = sf.Color.MAGENTA

		if self.rect == None: make_rect()
		if self.rect.size != self.size: make_rect()
		if self.rect.position != self.goto: make_rect()
		window.draw(self.rect)

###

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

class animation:
#Define an animation in advance, then watch it play.

	def __init__(self, MySprite):
		self._ = MySprite

		#	CLIP
		self.clips = []
		self.clip_interval = 0.5
		#
		self.clipClock = sf.Clock()
		self.clip_index = 0
		self.clip_init = True

	def play(self):


		#Keep resetting if there's no clips.
		if len(self.clips) == 0:
			self.clip_init = True
			self.clip_index = 0

		#Change clip
		if len(self.clips) != 0:

			#Immediately if it's just been initialized
			ticks = self.clipClock\
					.elapsed_time.as_seconds()

			if self.clip_init\
			or ticks > self.clip_interval:

				#Use the new clip.
				x, y = self.clips[self.clip_index]
				self._.clip.use(x, y)

				#Change the index.
				self.clip_index += 1
				if self.clip_index >= len(self.clips):
					self.clip_index = 0

				#Reset timer.
				self.clipClock.restart()
				self.clip_init = False

		#Check if the clip has gone out of the animation.
		#If so, stop animating.
		x, y = self._.clip.x, self._.clip.y
		if (x, y) not in self.clips:
			self.clips = []
	#


#	AXIS COLLISION

from modules.pysfml_game import Dot, Line

class AxisCollision:
#Collision detection designed for triangles.


	def __init__ (self, MySprite):
		self._ = MySprite
		self.z1, self.z2 = 0, 0 #Slope gradient.
		self.no1, self.no2 = 0, 0 #Order.


#	INITIALIZING
#	Creating the coordinates, lengths and angles.
#	Working out the order to create the slope gradient.

	class axis:
	#Each axis object.
		def __init__(self, name=None): self.name = name

		point = (0,0)
		angle = 0
		length = 0

	z1, z2 = 0, 0
	no1, no2 = None, None #The order to draw 
	def init_angles(self, Triangle, points=None):
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


		# WORK OUT ORDER
		#Calculates the triangle a single time.

		t = Triangle
		that = t.axis_collision
		r = self._

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

		that.no1, that.no2 = no1, no2
		that.x = x

	def observe_angles(self, Triangle):
	#Continous
	#Updates the z-axis for self.

		###COPY AND PASTED###
		r = self._
		t = Triangle
		that = t.axis_collision


		def sine_rule(a1, a2, l2):
		#Get the length.
			from math import sin, radians
			a1 = radians(a1); a2 = radians(a2)
			return (l2/sin(a2))*sin(a1)

		#Work out y from arbitary x.
		#Attach the first point to
		x1, y1 = that.no1.point
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		t_z1 = y2
		
		x1, y1 = that.no2.point
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		t_z2 = y2


		#The point order
		no1 = r.x1, r.y1
		no2 = r.x2, r.y2
		if r.x2 > that.x:
			no1 = r.x2, r.y1
			no2 = r.x1, r.y2

		#The lines
		x1, y1 = no1
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		z1 = y2

		x1, y1 = no2
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)		
		y2 = y1 - abs(_y2)
		z2 = y2
		####
		
		self.no1, self.no2 = no1, no2
		#
		that.z1, that.z2 = t_z1, t_z2
		self.z1, self.z2 = z1, z2


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


			print "ox", ox, "oy", oy, "oz", oz
			#SELECT the SMALLEST.
			smallest = abs(oz); use = oz

			if abs(oy) < smallest:
				ratio = Triangle.w/Triangle.h
				if abs(oy) < abs(oz)*ratio:
					smallest = abs(oy); use = oy

			#WIP###
			#If it's a z comparison
			if smallest == abs(oz):
				ratio = Triangle.w/Triangle.h
				# print "ox ",abs(ox), "  oz ",abs(oz)*ratio
				if abs(ox) < abs(oz)*ratio:
					smallest = abs(ox); use = ox
			####
			elif abs(ox) < smallest:
				smallest = abs(ox); use = ox

			#MOVE by the SMALLEST.
			if smallest == abs(oy):
				self._.move(0, use)
			elif smallest == abs(ox):
				self._.move(use, 0)
			elif smallest == abs(oz):
				self._.move(0, use)


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

		def sine_rule(a1, a2, l2):
		#Get the length.
			from math import sin, radians
			a1 = radians(a1); a2 = radians(a2)
			return (l2/sin(a2))*sin(a1)


		# ATTACH THE POINTS
		line_color = sf.Color.GREEN
		gap_color = sf.Color.BLACK
		
		#TRIANGLE
		x1, y1 = that.no1.point
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		that.line1 = Line(x1, y1, x2, y2, 3, line_color)
		that.z1 = y2
		
		x1, y1 = that.no2.point
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		that.line2 = Line(x1, y1, x2, y2, 3, line_color)
		that.z2 = y2

		that.line_gap = \
		Line(that.x, that.z1, that.x, that.z2, 5, gap_color)

		#RECTANGLE
		line_color = sf.Color.BLUE

		x1, y1 = self.no1
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)
		y2 = y1 - abs(_y2)
		self.line1 = Line(x1, y1, x2, y2, 3, line_color)
		self.z1 = y2

		x1, y1 = self.no2
		x2 = that.x
		_y2 = sine_rule(that.a.angle, that.c.angle, x2-x1)		
		y2 = y1 - abs(_y2)
		self.line2 = Line(x1, y1, x2, y2, 3, line_color)
		self.z2 = y2

		self.line_gap = \
		Line(that.x, self.z1, that.x, self.z2, 5, gap_color)

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