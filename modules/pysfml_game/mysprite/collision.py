class next:
#Collision is DEPENDANT.
#Provides positioning information about the next movement.
	
	def __init__(self, MySprite):
		self.x_move, self.y_move = 0, 0
		self._ = MySprite

	# STORE THEN CONFIRM
	x_move, y_move = 0, 0

	def store_move(self, x=None, y=None):
	#Store movement for later.
		if x == None: x = self.x_move
		if y == None: y = self.y_move
		self.x_move, self.y_move = x, y

	def confirm_move(self):
		self._.move(self.x_move, self.y_move)
		self.y_move, self.x_move = 0, 0
	#


	# POSITIONING (read-only)

	@property
	def stored_move(self): return self.x_move, self.y_move

	@property
	def x1(self): return self._.x1 + self.x_move
	@property
	def x2(self): return self._.x2 + self.x_move
	@property
	def y1(self): return self._.y1 + self.y_move
	@property
	def y2(self): return self._.y2 + self.y_move

	@property
	def position(self): return self.x1, self.y1
	@property
	def points(self):
		return self.x1, self.y1, self.x2, self.y2



class collision:
#Handles basic AABB collision checking.
#Checks X and Y individually.

	def __init__(self, MySprite):
		self._ = MySprite
		self.next = next(self._)

	#PUSHBACK
	# Clip any movements back which will result in a
	# collision.

	def pushback(self, ThatSprite):
		is_x = self.x_collision(ThatSprite)
		is_y = self.y_collision(ThatSprite)

		if is_x and is_y:
			ox = self.x_pushback(ThatSprite)
			oy = self.y_pushback(ThatSprite)

			nx, ny = self.next.stored_move
			if abs(ox - nx) < abs(oy - ny):
				self.next.x_move -= ox
			else:
				self.next.y_move -= oy
	#

	#Simply detects if there is any overlapping.
	def x_overlap(self, ThatSprite, predict=True):
		a = self._
		if predict: tx = self.next.x_move
		if not predict: tx = 0

		x1, x2 = ThatSprite.x1, ThatSprite.x2
		if x1 < a.x1+tx < x2: return True
		if x1 < a.x2+tx < x2: return True
		if a.x1+tx < x1 < a.x2+tx: return True
		if a.x1+tx < x2 < a.x2+tx: return True
		return False

	def y_overlap(self, ThatSprite, predict=True):
		a = self._
		if predict: ty = self.next.y_move
		if not predict: ty = 0

		y1, y2 = ThatSprite.y1, ThatSprite.y2
		if y1 < a.y1+ty < y2: return True
		if y1 < a.y2+ty < y2: return True
		if a.y1+ty < y1 < a.y2+ty: return True
		if a.y1+ty < y2 < a.y2+ty: return True
		return False

	#
	def x_collision(self, ThatSprite, predict=True):
		a = self._
		if predict: tx = self.next.x_move
		if not predict: tx = 0

		x1, x2 = ThatSprite.x1, ThatSprite.x2
		if x1 <= a.x1+tx <= x2: return True
		if x1 <= a.x2+tx <= x2: return True
		if a.x1+tx <= x1 <= a.x2+tx: return True
		if a.x1+tx <= x2 <= a.x2+tx: return True
		return False

	def y_collision(self, ThatSprite, predict=True):
		a = self._
		if predict: ty = self.next.y_move
		if not predict: ty = 0

		y1, y2 = ThatSprite.y1, ThatSprite.y2
		if y1 <= a.y1+ty <= y2: return True
		if y1 <= a.y2+ty <= y2: return True
		if a.y1+ty <= y1 <= a.y2+ty: return True
		if a.y1+ty <= y2 <= a.y2+ty: return True
		return False

	#

	#Works out the shortest pushback.
	def x_pushback(self, ThatSprite):
		a = self._
		tx = self.next.x_move
		p = []

		x1, x2 = ThatSprite.x1, ThatSprite.x2
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

	def y_pushback(self, ThatSprite):
		a = self._
		ty = self.next.y_move
		p = []
		
		y1, y2 = ThatSprite.y1, ThatSprite.y2
		if y1 <= a.y1+ty <= y2: p.append(y2 - a.y1)
		if y1 <= a.y2+ty <= y2: p.append(y1 - a.y2)
		if a.y1+ty <= y1 <= a.y2+ty: p.append(a.y1 - y2)
		if a.y1+ty <= y2 <= a.y2+ty: p.append(a.y2 - y1)

		lowest = None
		for i in p:
			if lowest == None: lowest = i
			if abs(i) <= lowest: lowest = i
		return ty - lowest


#####	Side Checks
#For resetting jumps, etc.

	def bottom_to_top(self, ThatSprite):
		if self.x_overlap(ThatSprite):
			if self._.y2 == ThatSprite.y1: return True
		return False

	def top_to_bottom(self, ThatSprite):
		if self.x_overlap(ThatSprite):
			if self._.y1 == ThatSprite.y2: return True
		return False

	def left_to_right(self, ThatSprite):
		if self.y_overlap(ThatSprite):
			if self._.x1 == ThatSprite.x2: return True
		return False

	def right_to_left(self, ThatSprite):
		if self.y_overlap(ThatSprite):
			if self._.x2 == ThatSprite.x1: return True
		return False
	#

####

from modules.pysfml_game import Dot
class slope_collision(object):
	def __init__(self, MySprite):
		self._ = MySprite
		self.next = self._.collision.next

		#Slope
		self.a, self.b = 0, 0
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

		is_x = AABB.x_collision(Slope)
		is_y = AABB.y_collision(Slope)
		is_z = self.is_z(Slope)

		if is_x and is_y and is_z:
			ox1 = AABB.x_pushback(Slope) #has tx/ty
			oy1 = AABB.y_pushback(Slope) #has tx/ty

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
				self.next.y_move -= small
			elif small == oy2:
				self.next.y_move -= small
			else:
				self.next.x_move -= small


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
		if predict:		tx,ty = self.next.stored_move
		if not predict: tx,ty = 0,0
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
		a, b = self._, triangle

		#Instant Cancels
		if self.next.y_move < 0: return False
		if a.x2 == b.x1: return False
		if b.x2 == a.x1: return False
		#

		if self._.collision\
		.x_collision(b, predict=False):

			#straight
			if b.slope_collision.anchor_y == "d":
				if int(self.y_overlap_amt\
					(b, predict=False)) == 0:
					return True

			#sloped
			if b.slope_collision.anchor_y == "u":
				if a.y2 == b.y1: return True

			#UNIQUE FIX
			if triangle.slope_collision.anchor_x == "r":
				if  b.x2 <= a.x2 and a.y2 == b.y1:
					return True

		return False


	def top_to_bottom(self, triangle):
		a, b = self._, triangle

		#Instant Cancels
		if a.x2 == b.x1: return False
		if b.x2 == a.x1: return False
		#

		if self._.collision\
		.x_collision(b, predict=False):

			if b.slope_collision.anchor_y == "d":
				if a.y1 == b.y2: return True

			if b.slope_collision.anchor_y == "u":
				if int(self.y_overlap_amt\
				(b, predict=False)) == 0:
					return True
		return False


	def left_to_right(self, triangle):
		a, b = self._, triangle

		#Instant Cancels
		if a.y2 == b.y1: return False
		if b.y2 == a.y1: return False
		#

		if self._.collision\
		.x_collision(b, predict=False):

			if b.slope_collision.anchor_x == "l":
				if a.x2 == b.x1: return True

			if b.slope_collision.anchor_x == "r":
				if int(self.y_overlap_amt\
				(b, predict=False)) == 0:
					return True
		return False


	def right_to_left(self, triangle):
		a, b = self._, triangle

		#Instant Cancels
		if a.y2 == b.y1: return False
		if b.y2 == a.y1: return False
		#

		if self._.collision\
		.y_collision(b, predict=False):

			if b.slope_collision.anchor_x == "l":
				if int(self.y_overlap_amt\
				(b, predict=False)) == 0:
					return True

			if b.slope_collision.anchor_x == "r":
				if a.x1 == b.x2: return True
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
		stx, sty = small.collision.next.stored_move
		btx, bty = big.collision.next.stored_move

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
		stx, sty = small.collision.next.stored_move
		btx, bty = big.collision.next.stored_move
		
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