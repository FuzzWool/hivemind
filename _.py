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

	def __init__(self): s = self

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
	def position(s, x, y): s.x, s.y = x, y

	#size
	@property
	def size(s): return s.w, s.h
	@size.setter
	def size(s, w, h): s.w, s.h = w, h

	#points
	@property
	def points(s): return s.x1,s.y1,s.x2,s.y2
	@points.setter
	def points(s,a,b,c,d): s.x1,s.y1,s.x2,s.y2 = a,b,c,d

	#center
	@property
	def center(s): return s.x+(s.w/2), s.y+(s.h/2)
	@center.setter
	def center(s,a,b): s.x,s.y = a-(s.w/2),b-(s.h/2)

	#### TILE
	
	#x
	@property
	def tile_x(self): return int(s.x/G)
	@tile_x.setter
	def tile_x(self,x): s.x = x*G
	#
	#y
	@property
	def tile_y(self): return int(s.y/G)
	@tile_y.setter
	def tile_y(self): s.y = y*G
	#
	#w
	@property
	def tile_w(self): return int(s.w/G)
	@tile_w.setter
	def tile_w(self): s.w = w*G
	#
	#h
	@property
	def tile_h(self): return int(s.h/G)
	@tile_h.setter
	def tile_h(self): s.h = h*G

	#x1
	#y1
	#x2
	#y2
	# position
	# size
	# points
	# center


	#### ROOM
	pass


r = GameRectangle()

r.x1, r.y1 = 100,100