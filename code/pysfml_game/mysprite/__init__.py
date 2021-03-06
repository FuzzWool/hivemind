
from loader import *

####

from code.pysfml_game.window import sf, window
from code.pysfml_game.geometry import GameRectangle
from code.pysfml_game import physics_animation
from collision import *

texture = sf.Texture.from_file
MyTexture = sf.Texture.from_file

class MySprite(sf.Sprite, GameRectangle):
#Provides additional functionality for sf.Sprite.
	def __init__ (self, arg):
		sf.Sprite.__init__(self, arg)
		self._w, self._h = 0, 0

		#States
		self.clip_enabled = False

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



	def draw(self, Camera=None):
		if self.texture == None: return

		if Camera == None:
			window.draw(self)

		#Draw only if it's within Camera bounds
		if Camera != None:
			if self.in_bounds(Camera):
				window.draw(self)

	#POSITIONING - linking inheritance + moving children

	@property
	def x(self): return self.position[0]
	@x.setter
	def x(self, x):
		for child in self.children:
			child.x += (x - self.x)
		self.position = x, self.y

	@property
	def y(self): return self.position[1]
	@y.setter
	def y(self, y):
		for child in self.children:
			child.y += (y - self.y)
		self.position = self.x, y

	@property
	def w(self):
		if self.clip_enabled: return self.clip.w
		if self.texture: return self.texture.size[0]
		else: return self._w
	@property
	def h(self):
		if self.clip_enabled: return self.clip.h
		if self.texture: return self.texture.size[1]
		else: return self._h
	#




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

		self._.clip_enabled = True

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

class box(GameRectangle):
#Handles the sprite's proportional positioning.
	def __init__ (self, mysprite):
		self._ = mysprite
		self.rect = None

		self.x, self.y, self.w, self.h = 0, 0, 0, 0

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
		if self.rect.position != self.position: make_rect()
		window.draw(self.rect)

###






class animation:
#Contains everything which may be animated.
	
	def __init__ (self, MySprite):
		self._ = MySprite

		#Position
		self.x = physics_animation()
		self.y = physics_animation()

		#Clipping
		self.clip = clip_animation(self._)

		#Colors
		self.red = physics_animation()
		self.green = physics_animation()
		self.blue = physics_animation()
		self.alpha = physics_animation()


	def play(self):
	#Play all animations.

		#Position
		self._.x += self.x.play(self._.x)
		self._.y += self.y.play(self._.y)

		#Clipping
		self.clip.play()

		#Colors
		r,g,b,a = self._.color
		r += self.red.play(r)
		g += self.green.play(g)
		b += self.blue.play(b)
		a += self.alpha.play(a)

		#don't go out of bounds
		def no_oob(color):
			if color < 0: color = 0
			if color > 255: color = 255
			return color
		r=no_oob(r); g=no_oob(g); b=no_oob(g); a=no_oob(a)

		self._.color = sf.Color(r,g,b,a)




class clip_animation:
#Plays a SEQUENCE of CLIPS.
#Refreshes whenether the clips change,
#but doesn't touch the CLIPS themselves.

	interval = 0.5
	clips = []
	loop = True

	def __init__(self, MySprite):
		self._ = MySprite
		self._refresh()

		self._old_clips = []
		self.clips = []
		self.loop = True
		#
		self.has_ended = False


	#


	@property
	def last_clip(self): #change clip
		return bool(self._index >= len(self.clips)-1)

	def play(self):
		if self._clips_changed()\
		or not self._are_clips():
			self._refresh()
			self._change_clip()

		if self._interval_hit()\
		and self._are_clips():
			self._change_clip()

		#

		if not self._clip_in_clips():
			self.clips = []


	# CONDITIONS

	def _clips_changed(self):
		changed = True
		if self._old_clips == self.clips:
			changed = False
		self._old_clips = self.clips
		return changed

	def _are_clips(self):
		return bool(len(self.clips) > 0)

	def _clip_in_clips(self):
		x, y = self._.clip.x, self._.clip.y
		this_clip = (x,y)
		return bool(this_clip in self.clips)


	interval_hit = False
	#
	def _interval_hit(self):
	#TRUE every time the clock hits the interval.
		seconds = self._clock.elapsed_time.seconds

		if seconds > self.interval:
			self._clock.restart()
			self.interval_hit = True
			return True
		self.interval_hit = False
		return False



	# ACTIONS

	def _refresh(self):
	#Restarts the animation class,
	#but DOESN'T do anything to the actual clip.

		#_may_progress
		self.interval = 0.5
		self._clock = sf.Clock()
		self._clock.restart()


		#_change_clip
		self._index = 0


	def _change_clip(self):
	#Increment the clip.

		if len(self.clips) != 0:
			
			if self._index < len(self.clips)-1:
				self._index += 1
			else:
				if self.loop: self._index = 0

			if not (self.has_ended and not self.loop):
				x, y = self.clips[self._index]
				self._.clip.use(x,y)

			if self.last_clip and not self.loop:
				self.has_ended = True
			else:
				self.has_ended = False