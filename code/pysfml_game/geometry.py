from window import GRID
from window import ROOM_WIDTH, ROOM_HEIGHT

#camera, room
class GameRectangle: #virtual
#Positioning based on TILES and ROOMS.

	# * RELIES ON x, y, w, h


	# ABSOLUTE

	@property
	def x1(self): return self.x
	@property
	def y1(self): return self.y
	@property
	def x2(self): return self.x + self.w
	@property
	def y2(self): return self.y + self.h

	@property
	def position(self): return self.x, self.y
	@property
	def size(self): return self.w, self.h
	@property
	def points(self): s=self; return s.x1, s.y1, s.x2, s.y2
	
	@property
	def center(self):
		s=self; return s.x+(s.w/2),s.y+(s.h/2)
	@center.setter
	def center(self, (x, y)):
		self.x = x-(self.w/2)
		self.y = y-(self.h/2)


	#

	def say_absolute(self):
		print "position", self.position
		print "size", self.size
		print "points", self.points
		print "center", self.center 


	def in_bounds(self, other):
		if self.y_in_bounds(other) \
		and self.x_in_bounds(other):
			return True

	def y_in_bounds(self, other):
		if self.y1 <= other.y1 <= self.y2: return True
		if self.y1 <= other.y2 <= self.y2: return True
		if other.y1 <= self.y1 <= other.y2: return True
		if other.y1 <= self.y2 <= other.y2: return True

		return False
	#
	def x_in_bounds(self, other):
		if self.x1 <= other.x1 <= self.x2: return True
		if self.x1 <= other.x2 <= self.x2: return True
		if other.x1 <= self.x1 <= other.x2: return True
		if other.x1 <= self.x2 <= other.x2: return True
		return False



	# TILE

	@property
	def tile_x(self): return int(self.x/GRID)
	@tile_x.setter
	def tile_x(self, x): self.x = x * GRID

	@property
	def tile_y(self): return int(self.y/GRID)
	@tile_y.setter
	def tile_y(self, y): self.y = y * GRID

	@property
	def tile_w(self): return int(self.w/GRID)
	@property
	def tile_h(self): return int(self.h/GRID)


	@property
	def tile_x1(self): return self.tile_x
	@property
	def tile_x2(self): return self.tile_x+self.tile_w+1
	@property
	def tile_y1(self): return self.tile_y
	@property
	def tile_y2(self): return self.tile_y+self.tile_h+1


	@property
	def tile_position(self): 
		return self.tile_x, self.tile_y
	@tile_position.setter
	def tile_position(self, pos):
		self.tile_x, self.tile_y = pos

	@property
	def tile_size(self):
		return self.tile_w, self.tile_h
	@property
	def tile_points(self):
		x1, y1, x2, y2 = self.points
		x1 = int(x1/GRID); y1 = int(y1/GRID)
		x2 = int(x2/GRID); y2 = int(y2/GRID)
		return x1, y1, x2, y2
	
	@property
	def tile_center(self):
		x, y = self.center
		x = int(x/GRID); y = int(y/GRID)
		return x, y

	#

	def keep_in_tile_size(self, w=None, h=None):
		if w != None:
			if w < 0: w = 0
			if w > self.tile_w: w = self.tile_w
		if h != None:
			if h < 0: h = 0
			if h > self.tile_h: h = self.tile_h

		if w != None and h != None: return w,h
		if w != None: return w
		if h != None: return h



	# ROOM

	@property
	def room_x(self):
		return int(self.x/ROOM_WIDTH)
	@room_x.setter
	def room_x(self, arg):
		self.x = arg * ROOM_WIDTH
		self.y = int(self.y/ROOM_HEIGHT) * ROOM_HEIGHT

	@property
	def room_y(self):
		return int(self.y/ROOM_HEIGHT)
	@room_y.setter
	def room_y(self, arg):
		self.x = int(self.x/ROOM_WIDTH) * ROOM_WIDTH
		self.y = arg * ROOM_HEIGHT

	@property
	def room_w(self): return int(self.w/ROOM_WIDTH)
	@property
	def room_h(self): return int(self.h/ROOM_HEIGHT)


	@property
	def room_x1(self): return self.room_x
	@property
	def room_x2(self): return self.room_x+self.room_w+1
	@property
	def room_y1(self): return self.room_y
	@property
	def room_y2(self): return self.room_y+self.room_h+1


	@property
	def room_position(self):return self.room_x,self.room_y
	@property
	def room_size(self):return self.room_w, self.room_h
	@property
	def room_center(self):
		s = self
		return s.room_x+(s.room_w/2),s.room_y+(s.room_h/2)
	@property
	def room_points(self):
		s = self
		return s.room_x1, s.room_y1, s.room_x2, s.room_y2




#	PHYSICAL
from window import sf, window
class Line:
#Create a line from one point to another.

	def __call__ (self): return self.vertices
	def __init__(self, x1, y1, x2, y2,\
				 w=1, color=sf.Color.RED):
		sfml = sf
		v = sfml.Vertex
		self.vertices = [v((x1-w, y1), color, (x2-w, y2)),
						 v((x2-w, y2), color, (x2+w, y2)),
						 v((x2+w, y2), color, (x1+w, y1)),
						 v((x1+w, y1), color, (x1-w, y1))]
	def draw(self):
		window.draw(self(), sf.QUADS)


#

class Dot(object):
	def __init__(self, radius=4):
		self.radius = radius
		self.color = sf.Color.RED

	#	SIZE

	_radius = 0
	@property
	def radius(self): return self._radius
	@radius.setter
	def radius(self, arg):
		self.dot = sf.CircleShape(arg)
		self._radius = arg

	#	POSITION

	@property
	def goto(self):
		pos = self.dot.position
		return pos[0], pos[1]
	@goto.setter
	def goto(self, args):
		self.dot.position = args[0], args[1]

	@property
	def center(self):
		x, y = self.goto
		r = self.radius
		return x+(r/2), y+(r/2)
	@center.setter
	def center(self, args):
		x, y = args
		r = self.radius
		self.goto = x-(r/2), y-(r/2)


	#	DRAWING

	_color = None
	@property
	def color(self): return self._color
	@color.setter
	def color(self, arg):
		self.dot.fill_color = arg
		self._color = arg
		#Outline
		self.dot.outline_thickness = 2
		self.dot.outline_color = sf.Color.WHITE

	def draw(self):
		window.draw(self.dot)