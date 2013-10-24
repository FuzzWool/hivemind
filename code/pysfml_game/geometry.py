from code.pysfml_game.window import GRID
from code.pysfml_game.window import ROOM_WIDTH,ROOM_HEIGHT

G = GRID
RX, RY = ROOM_WIDTH, ROOM_HEIGHT

class GameRectangle(object):

	#### ABSOLUTE
	x,y,w,h = 0,0,0,0

	# x1, y1, x2, y2
	# position
	# size
	# points
	# center

	# def __new__(self):
	# 	s = self

	#x1
	@property
	def x1(self): return self.x
	@x1.setter
	def x1(self, x1): self.x = x1
	#
	#y1
	@property
	def y1(self): return self.y
	@y1.setter
	def y1(self, y1): self.y = y1
	#
	#x2
	@property
	def x2(self): return self.x + self.w
	@x2.setter
	def x2(self, x2): self.x = x2 - self.w
	#
	#y2
	@property
	def y2(self): return self.y + self.h
	@y2.setter
	def y2(self, y2): self.y = y2 - self.h


	#position
	@property
	def position(self): return self.x, self.y
	@position.setter
	def position(self, args): self.x, self.y = args

	#size
	@property
	def size(self): return self.w, self.h
	@size.setter
	def size(self, args): self.w, self.h = args

	#points
	@property
	def points(self):
		return self.x1,self.y1,self.x2,self.y2
	@points.setter
	def points(self,args):
		self.x1,self.y1,self.x2,self.y2 = args

	#center
	@property
	def center(self):
		return self.x+(self.w/2), self.y+(self.h/2)
	@center.setter
	def center(self,a):
		self.x,self.y = a[0]-(self.w/2),a[1]-(self.h/2)


	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	#### TILE
	
	#x
	@property
	def tile_x(self): return int(self.x/G)
	@tile_x.setter
	def tile_x(self,x): self.x = x*G
	#
	#y
	@property
	def tile_y(self): return int(self.y/G)
	@tile_y.setter
	def tile_y(self,y): self.y = y*G
	#
	#w
	@property
	def tile_w(self): return int(self.w/G)
	@tile_w.setter
	def tile_w(self,w): self.w = w*G
	#
	#h
	@property
	def tile_h(self): return int(self.h/G)
	@tile_h.setter
	def tile_h(self,h): self.h = h*G

	####

	#x1
	@property
	def tile_x1(self): return self.tile_x
	@tile_x1.setter
	def tile_x1(self, x1): self.tile_x = x1
	#
	#y1
	@property
	def tile_y1(self): return self.tile_y
	@tile_y1.setter
	def tile_y1(self, y1): self.tile_y = y1
	#
	#x2
	@property
	def tile_x2(self): return self.tile_x + self.tile_w
	@tile_x2.setter
	def tile_x2(self, x2): self.tile_x = x2 - self.tile_w
	#
	#y2
	@property
	def tile_y2(self): return self.tile_y + self.tile_h
	@tile_y2.setter
	def tile_y2(self, y2): self.tile_y = y2 - self.tile_h


	#position
	@property
	def tile_position(self):
		return self.tile_x, self.tile_y
	@tile_position.setter
	def tile_position(self, args):
		self.tile_x, self.tile_y = args

	#size
	@property
	def tile_size(self): return self.tile_w, self.tile_h
	@tile_size.setter
	def tile_size(self, args):
		self.tile_w, self.tile_h = args

	#points
	@property
	def tile_points(self):
		return self.tile_x1,self.tile_y1,\
		self.tile_x2,self.tile_y2
	@tile_points.setter
	def tile_points(self,args):
		self.tile_x1,self.tile_y1,\
		self.tile_x2,self.tile_y2 = args

	#center
	@property
	def tile_center(self):
		return\
		self.tile_x+(self.tile_w/2),\
		self.tile_y+(self.tile_h/2)
	@tile_center.setter
	def tile_center(self,a):
		self.tile_x,self.tile_y = \
		a[0]-(self.tile_w/2), b[0]-(self.tile_h/2)



	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	#### ROOM

	#x
	@property
	def room_x(self): return int(self.x/RX)
	@room_x.setter
	def room_x(self,x): self.x = x*RX
	#
	#y
	@property
	def room_y(self): return int(self.y/RY)
	@room_y.setter
	def room_y(self,y): self.y = y*RY
	#
	#w
	@property
	def room_w(self): return int(self.w/RX)
	@room_w.setter
	def room_w(self,w): self.w = w*RX
	#
	#h
	@property
	def room_h(self): return int(self.h/RY)
	@room_h.setter
	def room_h(self,h): self.h = h*RY

	####

	#x1
	@property
	def room_x1(self): return self.room_x
	@room_x1.setter
	def room_x1(self, x1): self.room_x = x1
	#
	#y1
	@property
	def room_y1(self): return self.room_y
	@room_y1.setter
	def room_y1(self, y1): self.room_y = y1
	#
	#x2
	@property
	def room_x2(self):
		return self.room_x + self.room_w
	@room_x2.setter
	def room_x2(self, x2):
		self.room_x = x2 - self.room_w
	#
	#y2
	@property
	def room_y2(self):
		return self.room_y + self.room_h
	@room_y2.setter
	def room_y2(self, y2):
		self.room_y = y2 - self.room_h


	#position
	@property
	def room_position(self):
		return self.room_x, self.room_y
	@room_position.setter
	def room_position(self, args):
		self.room_x, self.room_y = args

	#size
	@property
	def room_size(self):
		return self.room_w, self.room_h
	@room_size.setter
	def room_size(self, args):
		self.room_w, self.room_h = args

	#points
	@property
	def room_points(self):
		return self.room_x1,self.room_y1,\
		self.room_x2,self.room_y2
	@room_points.setter
	def room_points(self,args):
		self.room_x1,self.room_y1,\
		self.room_x2,self.room_y2 = args

	#center
	@property
	def room_center(self):
		return\
		self.room_x+(self.room_w/2),\
		self.room_y+(self.room_h/2)
	@room_center.setter
	def room_center(self,a):
		self.room_x,self.room_y = \
		a[0]-(self.room_w/2), b[0]-(self.room_h/2)



	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	#### BOUNDS

	# bool in_points
	# function keep_in_points


	# IN_POINTS

	#private
	def _in_points(self, a_points, b_points):
		ax1, ay1, ax2, ay2 = a_points
		bx1, by1, bx2, by2 = b_points

		return self._in_x(ax1, ax2, bx1, bx2)\
		and    self._in_y(ay1, ay2, by1, by2)

	def _in_x(self, ax1, ax2, bx1, bx2):
		if ax1 <= bx1 <= ax2: return True
		if ax1 <= bx2 <= ax2: return True
		if bx1 <= ax1 <= bx2: return True
		if bx1 <= ax2 <= bx2: return True
		return False

	def _in_y(self, ay1, ay2, by1, by2):
		if ay1 <= by1 <= ay2: return True
		if ay1 <= by2 <= ay2: return True
		if by1 <= ay1 <= by2: return True
		if by1 <= ay2 <= by2: return True
		return False
	#


	# ABS
	def in_points(self, other):
		ax1,ay1,ax2,ay2 = self.points

		if tuple == type(other):
			if len(other) == 2:
				bx1,by1 = other
				bx2,by2 = other
			if len(other) == 4:
				bx1,by1,bx2,by2 = other
		else:
			bx1,by1,bx2,by2 = other.points
			
		a, b = (ax1,ay1,ax2,ay2),(bx1,by1,bx2,by2)
		return self._in_points(a, b)


	def in_x(self, b):
		#(x1,x2) or GameRectangle
		ax1, ax2 = self.x1, self.x2
		if tuple == type(other): bx1, bx2 = b[0], b[1]
		else: bx1, bx2 = b.x1, b.x2
		#
		return self._in_x(ax1, ax2, bx1, bx2)


	def in_y(self, other):
		ay1, ay2 = self.y1, self.y2
		if tuple == type(other): by1, by2 = b[0], b[1]
		else: by1, by2 = b.y1, b.y2
		
		return self._in_y(ay1, ay2, by1, by2)


	# TILE
	def in_tile_points(self, other):
		ax1,ay1,ax2,ay2 = self.tile_points

		if tuple == type(other):
			if len(other) == 2:
				bx1,by1 = other
				bx2,by2 = other
			if len(other) == 4:
				bx1,by1,bx2,by2 = other
		else:
			bx1,by1,bx2,by2 = other.tile_points

		a, b = (ax1,ay1,ax2,ay2),(bx1,by1,bx2,by2)
		return self._in_points(a, b)

	def in_tile_x(self):
		ax1, ax2 = self.tile_x1, self.tile_x2
		if tuple == type(other): bx1, bx2 = b[0], b[1]
		else: bx1, bx2 = b.tile_x1, b.tile_x2
		#
		return self._in_x(ax1, ax2, bx1, bx2)

	def in_tile_y(self):
		ay1, ay2 = self.tile_y1, self.tile_y2
		if tuple == type(other): by1, by2 = b[0], b[1]
		else: by1, by2 = b.tile_y1, b.tile_y2
		#
		return self._in_y(ay1, ay2, by1, by2)


	# ROOM
	def in_room_points(self, other):
		ax1,ay1,ax2,ay2 = self.room_points

		if tuple == type(other):
			if len(other) == 2:
				bx1,by1 = other
				bx2,by2 = other
			if len(other) == 4:
				bx1,by1,bx2,by2 = other
		else:
			bx1,by1,bx2,by2 = other.room_points
			
		a, b = (ax1,ay1,ax2,ay2),(bx1,by1,bx2,by2)
		return self._in_points(a, b)

	def in_room_x(self):
		ax1, ax2 = self.room_x1, self.room_x2
		if tuple == type(other): bx1, bx2 = b[0], b[1]
		else: bx1, bx2 = b.room_x1, b.room_x2
		#
		return self._in_x(ax1, ax2, bx1, bx2)

	def in_room_y(self):
		ay1, ay2 = self.room_y1, self.room_y2
		if tuple == type(other): by1, by2 = b[0], b[1]
		else: by1, by2 = b.room_y1, b.room_y2
		#
		return self._in_y(ay1, ay2, by1, by2)



	#

	# return value keep_in

	#private
	def _keep_in_z(self, left, value, right):
		if value < left: value = left
		if value > right: value = right
	#


	# ABS
	def keep_in_points(self, points):
		x1, y1, x2, y2 = points
		x1, x2 = self.keep_in_x(x1, x2)
		y1, y2 = self.keep_in_y(y1, y2)
		return x1, y1, x2, y2

	def keep_in_x(self, o):
		ax1, ax2 = self.x1, self.x2
		if tuple == type(o): bx1, bx2 = o
		else: bx1, bx2 = o.x1, o.x2

		bx1 = self._keep_in_z(ax1, bx1, ax2)
		bx2 = self._keep_in_z(ax1, bx2, ax2)
		return bx1, bx2

	def keep_in_y(self, o):
		ay1, ay2 = self.y1, self.y2
		if tuple == type(o): by1, by2 = o
		else: by1, by2 = o.y1, o.y2

		by1 = self._keep_in_z(ay1, by1, ay2)
		by2 = self._keep_in_z(ay1, by2, ay2)
		return by1, by2


	# TILE
	def keep_in_tile_points(self, points):
		x1, y1, x2, y2 = points
		x1, x2 = self.keep_in_tile_x(x1, x2)
		y1, y2 = self.keep_in_tile_y(y1, y2)
		return x1, y1, x2, y2

	def keep_in_tile_x(self, o):
		ax1, ax2 = self.tile_x1, self.tile_x2
		if tuple == type(o): bx1, bx2 = o
		else: bx1, bx2 = o.tile_x1, o.tile_x2

		bx1 = self._keep_in_z(ax1, bx1, ax2)
		bx2 = self._keep_in_z(ax1, bx2, ax2)
		return bx1, bx2

	def keep_in_tile_y(self, o):
		ay1, ay2 = self.tile_y1, self.tile_y2
		if tuple == type(o): by1, by2 = o
		else: by1, by2 = o.tile_y1, o.tile_y2

		by1 = self._keep_in_z(ay1, by1, ay2)
		by2 = self._keep_in_z(ay1, by2, ay2)
		return by1, by2


	# ROOM
	def keep_in_room_points(self, points):
		x1, y1, x2, y2 = points
		x1, x2 = self.keep_in_room_x(x1, x2)
		y1, y2 = self.keep_in_room_y(y1, y2)
		return x1, y1, x2, y2

	def keep_in_x(self, o):
		ax1, ax2 = self.room_x1, self.room_x2
		if tuple == type(o): bx1, bx2 = o
		else: bx1, bx2 = o.room_x1, o.room_x2

		bx1 = self._keep_in_z(ax1, bx1, ax2)
		bx2 = self._keep_in_z(ax1, bx2, ax2)
		return bx1, bx2

	def keep_in_room_y(self, o):
		ay1, ay2 = self.room_y1, self.room_y2
		if tuple == type(o): by1, by2 = o
		else: by1, by2 = o.room_y1, o.room_y2

		by1 = self._keep_in_z(ay1, by1, ay2)
		by2 = self._keep_in_z(ay1, by2, ay2)
		return by1, by2



	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	######################
	#### DEBUG

	def say_all(self):
		print "*** ABSOLUTE ***"
		s.say_abs()
		print "\n*** TILE ***"
		s.say_tile()
		print "\n*** ROOM ***"
		s.say_room()

	def say_abs(self):
		print "pos:	", s.position
		print "size:	", s.size
		print "points:	", s.points
		print "center:	", s.center

	def say_tile(self):
		print "pos:	",s.tile_position
		print "size:	",s.tile_size
		print "points:	",s.tile_points
		print "center:	",s.tile_center


	def say_room(self):
		print "pos:	",s.room_position
		print "size:	",s.room_size
		print "points:	",s.room_points
		print "center:	",s.room_center






######################
######################
######################
######################
######################
######################
######################
######################
######################
######################
######################

######################

######################

######################
######################
######################
######################
######################
######################
######################
######################
######################
######################


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