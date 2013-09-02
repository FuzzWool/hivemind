from window import sf, window
from geometry import Rectangle

texture = sf.Texture.from_file
MyTexture = sf.Texture.from_file

class MySprite(sf.Sprite, Rectangle):
#Provides additional functionality for sf.Sprite.
	def __init__ (self, arg):
		sf.Sprite.__init__(self, arg)
		
		#All sub-classes
		self.resize = resize(self)
		self.clip = clip(self)
		self.box = box(self)
		self.children = []; self.children_class = children_class(self)
		self.animation = animation(self)
		self.collision = collision(self)
		self.slope_collision = slope_collision(self)
		self.overlap = overlap(self)

	#Positioning is handled by goto instead of position.
	#Position can't be overriden, but it needs to be for children.
	@property
	def goto(self):
		return self.position[0], self.position[1]
				# - (self.origin[0] * self.scale(0)),\
				# - (self.origin[1] * self.scale[1])
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
		if w != 0 and self._.w != 0:
			rw = w / self._.w
			#
			if to_scale == False:
				rh = 1
			else:
				rh = rw
			#
			self._.scale(rw)

	def h(self, h, to_scale = True):
		if h != 0 and self._.h != 0:
			rh = h / self._.h
			#
			if to_scale == False:
				rw = 1
			else:
				rw = rh
			#
			self._.scale(rh)


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
		self._.texture_rectangle = (x, y, w, h)

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
		self._.texture_rectangle = (x1, y1, x2, y2)


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
		if self._.h != 0:
			proportion = arg / self._.w
			for s in self._.children:
				s.w = proportion * s.w

	def h(self, arg):
		if self._.h != 0:
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
					.elapsed_time.seconds

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

		#Instant Cancels
		if self._.collision.ty < 0: return False
		#


		if self._.collision\
		.x_collision(x1, x2, predict=False):
			
			#straight
			if triangle.slope_collision.anchor_y == "d":
				if self.y_overlap_amt(triangle, predict=False) == 0:
					return True

			#sloped
			if triangle.slope_collision.anchor_y == "u":
				if self._.y2 == triangle.y1:
					return True

			#UNIQUE FIX
			if triangle.slope_collision.anchor_x == "r":
				if  triangle.x2 <= self._.x2\
				and self._.y2 == triangle.y1:
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
				if self.y_overlap_amt(triangle, predict=False) == 0:
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
				if self.y_overlap_amt(triangle, predict=False) == 0:
					return True
		return False


	def right_to_left(self, triangle):
		x1, y1, x2, y2 = triangle.points

		if self._.collision\
		.y_collision(y1, y2, predict=False):

			if triangle.slope_collision.anchor_x == "l":
				if self.y_overlap_amt(triangle, predict=False) == 0:
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
			self.adot = Dot(); self.adot.goto = self.a
			self.bdot = Dot(); self.bdot.goto = self.b
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