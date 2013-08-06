#	VIRTUAL
class Rectangle(object):
#A class designed to be used with pySFML's transformable.
#Goto is used instead of position, because position cannot be overriden.
	
	position = [0, 0]
	w, h = 0, 0

	@property
	def x(self): return self.goto[0]
	@x.setter
	def x(self, x): self.goto = x, self.y

	@property
	def y(self): return self.goto[1]
	@y.setter
	def y(self, y): self.goto = self.x, y

	#

	@property
	def boundary(self): return self.goto[0], self.goto[1], self.w, self.h
	@boundary.setter
	def boundary(self, args):
		self.goto = args[:2]
		self.size = args[2:]

	@property
	def goto(self): return self.position
	@goto.setter
	def goto(self, args):
		self.position = args

	@property
	def size(self): return self.w, self.h
	@size.setter
	def size(self, args):
		self.w, self.h = args

	@property
	def points(self): return self.goto[0], self.goto[1], self.goto[0] + self.w, self.goto[1] + self.h
	@points.setter
	def points(self, args):
		self.goto = args[0], args[1]
		self.w, self.h = args[2] - args[0], args[3] - args[1]

	@property
	def center(self): return self.goto[0] + (self.w/2), self.goto[1] + (self.h/2)
	@center.setter
	def center(self, args):
		self.goto = args[0] - (self.w/2), args[1] - (self.h/2) 

	def debug(self):
		print "x", self.goto[0], "y", self.goto[1], "w", self.w, "h", self.h
		print "boundary", self.boundary
		print "goto", self.goto, "size", self.size
		print "points", self.points


	#	POINTS
	@property
	def x1(self): return self.x
	@x1.setter
	def x1(self, arg): self.x = arg

	@property
	def y1 (self): return self.y
	@y1.setter
	def y1 (self, arg): self.y = arg

	@property
	def x2(self): return self.x + self.w
	@x2.setter
	def x2(self, arg): self.x = arg - self.w

	@property
	def y2(self): return self.y + self.h
	@y2.setter
	def y2(self, arg): self.y = arg - self.h


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