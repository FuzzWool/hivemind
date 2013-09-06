from collision import *
#=======================

from modules.pysfml_game.window import sf, window
from modules.pysfml_game.geometry import Rectangle

texture = sf.Texture.from_file
MyTexture = sf.Texture.from_file

class MySprite(sf.Sprite, Rectangle):
#Provides additional functionality for sf.Sprite.
	def __init__ (self, arg):
		sf.Sprite.__init__(self, arg)
		
		#General sub-classes.
		self.resize = resize(self)
		self.clip = clip(self)
		self.box = box(self)
		self.children = []; self.children_class = children_class(self)
		self.animation = animation(self)

		#Collision sub-classes.
		self.overlap = overlap(self)
		self.collision = collision(self)
		self.slope_collision = slope_collision(self)

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

