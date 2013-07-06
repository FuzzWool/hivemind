from window import sf, window
from geometry import Rectangle

class MySprite(sf.Sprite, Rectangle):
#Provides additional functionality for sf.Sprite.
	def __init__ (self, arg):
		sf.Sprite.__init__(self, arg)
		
		#All sub-classes
		self.resize = resize(self)
		self.clip = clip(self)
		self.box = box(self)
		self.children = []; self.children_class = children_class(self)

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
#Saves grid size, chooses grid position. For spritesheets.
	def __init__ (self, MySprite):
		self._ = MySprite
		self.ox, self.oy, self.w, self.h = 0, 0, 0, 0
		self.x, self.y = 0, 0

	def __call__ (self, *args): self.set(*args)
	def set(self, w, h, x=0, y=0): #Absolute
		self.w, self.h, self.ox, self.oy = w, h, x, y
		self._.set_texture_rect(\
			sf.IntRect(x, y, w, h))

	def division(self, x, y): #Relative
		w, h = self._.w / x, self._.h / y
		self.set(w, h)

	def use(self, x=-1, y=-1):
		if x == -1: x = self.x
		if y == -1: y = self.y
		self.x, self.y = x, y
		ox, oy, w, h = self.ox, self.oy, self.w, self.h
		self._.set_texture_rect(sf.IntRect\
			(ox+(w*x), oy+(h*y), w, h))



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


class animation:
#Define an animation in advance, then watch it play.
	pass