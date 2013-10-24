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

	def __init__(self, x=0, y=0, w=0, h=0):
		s = self
		s.x, s.y, s.w, s.h = x, y, w, h


	#x1
	@property
	def x1(s): return s.x
	@x1.setter
	def x1(s, x1): s.x = x1
	#
	#y1
	@property
	def y1(s): return s.y
	@y1.setter
	def y1(s, y1): s.y = y1
	#
	#x2
	@property
	def x2(s): return s.x + s.w
	@x2.setter
	def x2(s, x2): s.x = x2 - s.w
	#
	#y2
	@property
	def y2(s): return s.y + s.h
	@y2.setter
	def y2(s, y2): s.y = y2 - s.h


	#position
	@property
	def position(s): return s.x, s.y
	@position.setter
	def position(s, args): s.x, s.y = args

	#size
	@property
	def size(s): return s.w, s.h
	@size.setter
	def size(s, args): s.w, s.h = args

	#points
	@property
	def points(s): return s.x1,s.y1,s.x2,s.y2
	@points.setter
	def points(s,args): s.x1,s.y1,s.x2,s.y2 = args

	#center
	@property
	def center(s): return s.x+(s.w/2), s.y+(s.h/2)
	@center.setter
	def center(s,a): s.x,s.y = a[0]-(s.w/2),a[1]-(s.h/2)


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
	def tile_x(s): return int(s.x/G)
	@tile_x.setter
	def tile_x(s,x): s.x = x*G
	#
	#y
	@property
	def tile_y(s): return int(s.y/G)
	@tile_y.setter
	def tile_y(s,y): s.y = y*G
	#
	#w
	@property
	def tile_w(s): return int(s.w/G)
	@tile_w.setter
	def tile_w(s,w): s.w = w*G
	#
	#h
	@property
	def tile_h(s): return int(s.h/G)
	@tile_h.setter
	def tile_h(s,h): s.h = h*G

	####

	#x1
	@property
	def tile_x1(s): return s.tile_x
	@tile_x1.setter
	def tile_x1(s, x1): s.tile_x = x1
	#
	#y1
	@property
	def tile_y1(s): return s.tile_y
	@tile_y1.setter
	def tile_y1(s, y1): s.tile_y = y1
	#
	#x2
	@property
	def tile_x2(s): return s.tile_x + s.tile_w
	@tile_x2.setter
	def tile_x2(s, x2): s.tile_x = x2 - s.tile_w
	#
	#y2
	@property
	def tile_y2(s): return s.tile_y + s.tile_h
	@tile_y2.setter
	def tile_y2(s, y2): s.tile_y = y2 - s.tile_h


	#position
	@property
	def tile_position(s): return s.tile_x, s.tile_y
	@tile_position.setter
	def tile_position(s, args): s.tile_x, s.tile_y = args

	#size
	@property
	def tile_size(s): return s.tile_w, s.tile_h
	@tile_size.setter
	def tile_size(s, args): s.tile_w, s.tile_h = args

	#points
	@property
	def tile_points(s):
		return s.tile_x1,s.tile_y1,s.tile_x2,s.tile_y2
	@tile_points.setter
	def tile_points(s,args):
		s.tile_x1,s.tile_y1,s.tile_x2,s.tile_y2 = args

	#center
	@property
	def tile_center(s):
		return\
		s.tile_x+(s.tile_w/2), s.tile_y+(s.tile_h/2)
	@tile_center.setter
	def tile_center(s,a):
		s.tile_x,s.tile_y = \
		a[0]-(s.tile_w/2), b[0]-(s.tile_h/2)



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
	def room_x(s): return int(s.x/RX)
	@room_x.setter
	def room_x(s,x): s.x = x*RX
	#
	#y
	@property
	def room_y(s): return int(s.y/RY)
	@room_y.setter
	def room_y(s,y): s.y = y*RY
	#
	#w
	@property
	def room_w(s): return int(s.w/RX)
	@room_w.setter
	def room_w(s,w): s.w = w*RX
	#
	#h
	@property
	def room_h(s): return int(s.h/RY)
	@room_h.setter
	def room_h(s,h): s.h = h*RY

	####

	#x1
	@property
	def room_x1(s): return s.room_x
	@room_x1.setter
	def room_x1(s, x1): s.room_x = x1
	#
	#y1
	@property
	def room_y1(s): return s.room_y
	@room_y1.setter
	def room_y1(s, y1): s.room_y = y1
	#
	#x2
	@property
	def room_x2(s): return s.room_x + s.room_w
	@room_x2.setter
	def room_x2(s, x2): s.room_x = x2 - s.room_w
	#
	#y2
	@property
	def room_y2(s): return s.room_y + s.room_h
	@room_y2.setter
	def room_y2(s, y2): s.room_y = y2 - s.room_h


	#position
	@property
	def room_position(s): return s.room_x, s.room_y
	@room_position.setter
	def room_position(s, args): s.room_x, s.room_y = args

	#size
	@property
	def room_size(s): return s.room_w, s.room_h
	@room_size.setter
	def room_size(s, args): s.room_w, s.room_h = args

	#points
	@property
	def room_points(s):
		return s.room_x1,s.room_y1,s.room_x2,s.room_y2
	@room_points.setter
	def room_points(s,args):
		s.room_x1,s.room_y1,s.room_x2,s.room_y2 = args

	#center
	@property
	def room_center(s):
		return\
		s.room_x+(s.room_w/2), s.room_y+(s.room_h/2)
	@room_center.setter
	def room_center(s,a):
		s.room_x,s.room_y = \
		a[0]-(s.room_w/2), b[0]-(s.room_h/2)



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
	def _in_points(s, a_points, b_points):
		ax1, ay1, ax2, ay2 = a_points
		bx1, by1, bx2, by2 = b_points

		return s._in_x(ax1, ax2, bx1, bx2)\
		and    s._in_y(ay1, ay2, by1, by2)

	def _in_x(s, ax1, ax2, bx1, bx2):
		if ax1 <= bx1 <= ax2: return True
		if ax1 <= bx2 <= ax2: return True
		if bx1 <= ax1 <= bx2: return True
		if bx1 <= ax2 <= bx2: return True
		return False

	def _in_y(s, ay1, ay2, by1, by2):
		if ay1 <= by1 <= ay2: return True
		if ay1 <= by2 <= ay2: return True
		if by1 <= ay1 <= by2: return True
		if by1 <= ay2 <= by2: return True
		return False
	#


	# ABS
	def in_points(s, other):
		a, b = s, other
		return s._in_points(a.points, b.points)


	def in_x(self, b):
		#(x1,x2) or GameRectangle
		ax1, ax2 = self.x1, self.x2
		if list == type(other): bx1, bx2 = b[0], b[1]
		else: bx1, bx2 = b.x1, b.x2
		#
		return self._in_x(ax1, ax2, bx1, bx2)


	def in_y(self, other):
		ay1, ay2 = self.y1, self.y2
		if list == type(other): by1, by2 = b[0], b[1]
		else: by1, by2 = b.y1, b.y2
		
		return self._in_y(ay1, ay2, by1, by2)


	# TILE
	def in_tile_points(self, other):
		a, b = s.tile_points, other.tile_points
		return s._in_points(a, b)

	def in_tile_x(self):
		ax1, ax2 = self.tile_x1, self.tile_x2
		if list == type(other): bx1, bx2 = b[0], b[1]
		else: bx1, bx2 = b.tile_x1, b.tile_x2
		#
		return self._in_x(ax1, ax2, bx1, bx2)

	def in_tile_y(self):
		ay1, ay2 = self.tile_y1, self.tile_y2
		if list == type(other): by1, by2 = b[0], b[1]
		else: by1, by2 = b.tile_y1, b.tile_y2
		#
		return self._in_y(ay1, ay2, by1, by2)


	# ROOM
	def in_room_points(self, other):
		a, b = s.room_points, other.room_points
		return s._in_points(a, b)

	def in_room_x(self):
		ax1, ax2 = self.room_x1, self.room_x2
		if list == type(other): bx1, bx2 = b[0], b[1]
		else: bx1, bx2 = b.room_x1, b.room_x2
		#
		return self._in_x(ax1, ax2, bx1, bx2)

	def in_room_y(self):
		ay1, ay2 = self.room_y1, self.room_y2
		if list == type(other): by1, by2 = b[0], b[1]
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
		if list == type(o): bx1, bx2 = o
		else: bx1, bx2 = o.x1, o.x2

		bx1 = self._keep_in_z(ax1, bx1, ax2)
		bx2 = self._keep_in_z(ax1, bx2, ax2)
		return bx1, bx2

	def keep_in_y(self, o):
		ay1, ay2 = self.y1, self.y2
		if list == type(o): by1, by2 = o
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
		if list == type(o): bx1, bx2 = o
		else: bx1, bx2 = o.tile_x1, o.tile_x2

		bx1 = self._keep_in_z(ax1, bx1, ax2)
		bx2 = self._keep_in_z(ax1, bx2, ax2)
		return bx1, bx2

	def keep_in_tile_y(self, o):
		ay1, ay2 = self.tile_y1, self.tile_y2
		if list == type(o): by1, by2 = o
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
		if list == type(o): bx1, bx2 = o
		else: bx1, bx2 = o.room_x1, o.room_x2

		bx1 = self._keep_in_z(ax1, bx1, ax2)
		bx2 = self._keep_in_z(ax1, bx2, ax2)
		return bx1, bx2

	def keep_in_room_y(self, o):
		ay1, ay2 = self.room_y1, self.room_y2
		if list == type(o): by1, by2 = o
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

	def say_all(s):
		print "*** ABSOLUTE ***"
		s.say_abs()
		print "\n*** TILE ***"
		s.say_tile()
		print "\n*** ROOM ***"
		s.say_room()

	def say_abs(s):
		print "pos:	", s.position
		print "size:	", s.size
		print "points:	", s.points
		print "center:	", s.center

	def say_tile(s):
		print "pos:	",s.tile_position
		print "size:	",s.tile_size
		print "points:	",s.tile_points
		print "center:	",s.tile_center


	def say_room(s):
		print "pos:	",s.room_position
		print "size:	",s.room_size
		print "points:	",s.room_points
		print "center:	",s.room_center



r = GameRectangle(50,50,800,100)
r2 = GameRectangle(50,0,100,0)