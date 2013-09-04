class collision:
#Handles basic AABB collision checking.
#Checks X and Y individually.

	def __init__(self, MySprite):
		self._ = MySprite


	#PUSHBACK
	# Clip any movements back which will result in a
	# collision.

	tx, ty = 0, 0
	def try_move(self, x=None, y=None):
		if x == None: x = self.tx
		if y == None: y = self.ty
		self.tx = x
		self.ty = y

	def pushback(self, ThatSprite):
		x1, y1, x2, y2 = ThatSprite.points
		is_x = self.x_collision(x1, x2)
		is_y = self.y_collision(y1, y2)

		if is_x and is_y:
			ox = self.x_pushback(x1, x2)
			oy = self.y_pushback(y1, y2)

			if abs(ox - self.tx) < abs(oy - self.ty):
				self.tx -= ox
			else:
				self.ty -= oy

	def confirm_move(self):
		self._.move(self.tx, self.ty)
		self.tx, self.ty = 0, 0

	#

	#Simply detects if there is any overlapping.
	def x_overlap(self, x1, x2, predict=True):
		a = self._
		if predict: tx = self.tx
		if not predict: tx = 0

		if x1 < a.x1+tx < x2: return True
		if x1 < a.x2+tx < x2: return True
		if a.x1+tx < x1 < a.x2+tx: return True
		if a.x1+tx < x2 < a.x2+tx: return True
		return False

	def y_overlap(self, y1, y2, predict=True):
		a = self._
		if predict: ty = self.ty
		if not predict: ty = 0

		if y1 < a.y1+ty < y2: return True
		if y1 < a.y2+ty < y2: return True
		if a.y1+ty < y1 < a.y2+ty: return True
		if a.y1+ty < y2 < a.y2+ty: return True
		return False

	#
	def x_collision(self, x1, x2, predict=True):
		a = self._
		if predict: tx = self.tx
		if not predict: tx = 0

		if x1 <= a.x1+tx <= x2: return True
		if x1 <= a.x2+tx <= x2: return True
		if a.x1+tx <= x1 <= a.x2+tx: return True
		if a.x1+tx <= x2 <= a.x2+tx: return True
		return False

	def y_collision(self, y1, y2, predict=True):
		a = self._
		if predict: ty = self.ty
		if not predict: ty = 0

		if y1 <= a.y1+ty <= y2: return True
		if y1 <= a.y2+ty <= y2: return True
		if a.y1+ty <= y1 <= a.y2+ty: return True
		if a.y1+ty <= y2 <= a.y2+ty: return True
		return False

	#

	#Works out the shortest pushback.
	def x_pushback(self, x1, x2):
		a = self._
		tx = self.tx
		p = []

		if x1 <= a.x1+tx <= x2: p.append(x2 - a.x1)
		if x1 <= a.x2+tx <= x2: p.append(x1 - a.x2)
		if a.x1+tx <= x1 <= a.x2+tx: p.append(a.x1 - x2)
		if a.x1+tx <= x2 <= a.x2+tx: p.append(a.x2 - x1)

		lowest = None
		for i in p:
			if lowest == None: lowest = i
			if abs(i) <= lowest: lowest = i
		if lowest != None:
			return tx - lowest

	def y_pushback(self, y1, y2):
		a = self._
		ty = self.ty
		p = []
		
		if y1 <= a.y1+ty <= y2: p.append(y2 - a.y1)
		if y1 <= a.y2+ty <= y2: p.append(y1 - a.y2)
		if a.y1+ty <= y1 <= a.y2+ty: p.append(a.y1 - y2)
		if a.y1+ty <= y2 <= a.y2+ty: p.append(a.y2 - y1)

		lowest = None
		for i in p:
			if lowest == None: lowest = i
			if abs(i) <= lowest: lowest = i
		return ty - lowest


#####	Extra checks
#For resetting jumps, etc.

	#Side checks.
	def bottom_to_top(self, x1, y1, x2, y2):
	#If a's bottom is colliding with b's top.
		if self.x_overlap(x1, x2):
			a = self._
			if a.y2 == y1: return True
		return False

	def top_to_bottom(self, x1, y1, x2, y2):
		if self.x_overlap(x1, x2):
			a = self._
			if a.y1 == y2: return True
		return False

	def left_to_right(self, x1, y1, x2, y2):
		if self.y_overlap(y1, y2):
			a = self._
			if a.x1 == x2: return True
		return False

	def right_to_left(self, x1, y1, x2, y2):
		if self.y_overlap(y1, y2):
			a = self._
			if a.x2 == x1: return True
		return False
	#

####

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

	#	POSITION

	#wip
	@property
	def left_point(self):
		if self.a[0] < self.b[0]:
			return self.a
		return self.b

	@property
	def right_point(self):
		if self.a[0] > self.b[0]:
			return self.a
		return self.b

	@property
	def up_point(self):
		if self.a[1] < self.b[1]:
			return self.a
		return self.b

	@property
	def down_point(self):
		if self.a[1] > self.b[1]:
			return self.a
		return self.b
	#


	#	COLLISION

	def pushback(self, Slope):
	#Against a slope with it's A and B set.
	#Borrows from MySprite.collision
		x1, y1, x2, y2 = Slope.points
		AABB = self._.collision

		is_x = AABB.x_collision(x1, x2)
		is_y = AABB.y_collision(y1, y2)
		is_z = self.is_z(Slope)

		if is_x and is_y and is_z:
			ox1 = AABB.x_pushback(x1, x2) #has tx/ty
			oy1 = AABB.y_pushback(y1, y2) #has tx/ty

			#The slope's pushback's positivity depends
			#on anchor.
			that = Slope.slope_collision
			oy2 = self.y_overlap_amt(Slope)

			#FIND the smallest pushback.
			small = oy2
			if abs(ox1) < abs(oy2):
				small = ox1
			#
			if small == oy2:
				if abs(oy1) < abs(oy2):
					small = oy1
			if small == ox1:
				if abs(oy1) < abs(ox1):
					small = oy1

			#MOVE BY the smallest pushback.
			if small == oy1:
				self._.collision.ty -= small
			elif small == oy2:
				self._.collision.ty -= small
			else:
				self._.collision.tx -= small


	def is_z(self, Slope):
		z = self.y_overlap_amt(Slope)
		that = Slope.slope_collision
		if that.anchor in ["rd", "ld"]:
			return bool(0 < z)

		if that.anchor in ["ru", "lu"]:
			return bool(z < 0)

	def y_overlap_amt(self, Slope, predict=True):
	#Returns a positive value.
		that = Slope.slope_collision

		#WIP
		if predict:
			tx,ty = self._.collision.tx,self._.collision.ty
		if not predict:
			tx,ty = 0,0
		#

		#Gradient
		w = that.b[0] - that.a[0]; w = abs(w)
		h = that.b[1] - that.a[1]; h = abs(h)
		ratio = h/w

		#X from origin
		y_lowering = self._.x2 - that.a[0] + tx
		y_lowering *= ratio

		if that.anchor == "rd":
			if h <= y_lowering: y_lowering = h
			gap = self._.y2 - that.a[1] + ty
			return (gap + y_lowering)

		if that.anchor == "ru":
			if 0 <= y_lowering: y_lowering = 0
			gap = self._.y1 - that.a[1] + ty
			return (gap - y_lowering)


		y_lowering = self._.x1 - Slope.x1 + tx
		y_lowering *= ratio

		if that.anchor == "ld":
			if y_lowering <= 0: y_lowering = 0
			gap = self._.y2 - that.a[1] + ty
			return (gap - y_lowering)

		if that.anchor == "lu":
			if y_lowering <= 0: y_lowering = 0
			gap = self._.y1 - that.a[1] + ty
			return (gap + y_lowering)
	#


	#####	Extra checks
	#For resetting jumps, etc.

	#Side checks.
	def bottom_to_top(self, triangle):
	#If a's bottom is colliding with b's top.
		x1, y1, x2, y2 = triangle.points
		y1 = triangle.slope_collision.up_point[0]
		y2 = triangle.slope_collision.down_point[0]


		#Instant Cancels
		if self._.collision.ty < 0: return False
		#


		if self._.collision\
		.x_collision(x1, x2, predict=False):

			#straight
			if triangle.slope_collision.anchor_y == "d":

				if int(self.y_overlap_amt\
					(triangle, predict=False)) == 0:
					return True

			#sloped
			if triangle.slope_collision.anchor_y == "u":
				if self._.y2 == y1:
					return True

			#UNIQUE FIX
			if triangle.slope_collision.anchor_x == "r":
				if  triangle.x2 <= self._.x2\
				and self._.y2 == y1:
					print "PROBLEM"
					return True

		return False


	def top_to_bottom(self, triangle):
		x1, y1, x2, y2 = triangle.points

		if self._.collision\
		.x_collision(x1, x2, predict=False):

			if triangle.slope_collision.anchor_y == "d":
				if self._.y1 == triangle.y2:
					return True

			if triangle.slope_collision.anchor_y == "u":
				if int(self.y_overlap_amt\
				(triangle, predict=False)) == 0:
					return True
		return False


	def left_to_right(self, triangle):
		x1, y1, x2, y2 = triangle.points
		
		if self._.collision\
		.y_collision(y1, y2, predict=False):

			if triangle.slope_collision.anchor_x == "l":
				if self._.x2 == triangle.x1:
					return True

			if triangle.slope_collision.anchor_x == "r":
				if int(self.y_overlap_amt\
				(triangle, predict=False)) == 0:
					return True
		return False


	def right_to_left(self, triangle):
		x1, y1, x2, y2 = triangle.points

		if self._.collision\
		.y_collision(y1, y2, predict=False):

			if triangle.slope_collision.anchor_x == "l":
				if int(self.y_overlap_amt\
				(triangle, predict=False)) == 0:
					return True

			if triangle.slope_collision.anchor_x == "r":
				if self._.x1 == triangle.x2:
					return True
		return False
	#

	# VISUAL DEBUG

	adot, bdot = None, None
	def draw(self):
		#Make the dots.
		if (self.adot, self.bdot) == (None, None):
			self.adot = Dot(1); self.adot.goto = self.a
			self.bdot = Dot(1); self.bdot.goto = self.b
		#Draw the dots.
		self.adot.draw(); self.bdot.draw()


class overlap:
	def __init__ (self, MySprite): self._ = MySprite

	def x(self, ThatSprite):


		sprite1, sprite2 = self._, ThatSprite
		if sprite2.w > sprite1.w:
			big, small = sprite2, sprite1
		else:
			big, small = sprite1, sprite2
		
		#Next move.
		stx, sty = small.collision.tx, small.collision.ty
		btx, bty = big.collision.tx, big.collision.ty

		#Choose which SIDE to return based on the CENTER.
		o = small.center[0]+stx - big.center[0]+bty

		if o <= 0:
			left_gap = small.x2+stx - big.x1-btx
			if left_gap > small.w: left_gap = small.w
			return left_gap
		if o >  0:
			right_gap = big.x2+btx - small.x1-stx
			if right_gap > small.w: right_gap = small.w
			return right_gap


	def y(self, ThatSprite):
		sprite1, sprite2 = self._, ThatSprite

		if sprite2.h > sprite1.h:
			big, small = sprite2, sprite1
		else:
			big, small = sprite1, sprite2
		
		#Next move.
		stx, sty = small.collision.tx, small.collision.ty
		btx, bty = big.collision.tx, big.collision.ty
		
		o = small.center[1]+sty - big.center[1]+bty

		if o <= 0:
			up_gap = small.y2+sty - big.y1-bty
			if up_gap > small.h: up_gap = small.h
			gap = up_gap
		if o >  0:
			down_gap = big.y2+bty - small.y1-sty
			if down_gap > small.h: down_gap = small.h
			gap = down_gap

		return gap