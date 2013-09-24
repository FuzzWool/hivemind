from window import sf
from window import window as the_window
from window import SCREEN_HEIGHT, SCREEN_WIDTH
from window import ROOM_WIDTH, ROOM_HEIGHT
from window import GRID

from geometry import GameRectangle

class MyCamera(sf.View, GameRectangle):

	#Default settings.
	#2:1 scale
	def __init__(self):
		sf.View.__init__(self)
		self.zoom = float(2)
		self.center = the_window.view.center

	# ZOOM
	_zoom = float(1)
	
	@property
	def zoom(self): return self._zoom
	@zoom.setter
	def zoom(self, ratio):
		self._zoom = float(ratio)
		#
		w, h = SCREEN_WIDTH, SCREEN_HEIGHT
		w /= ratio; h /= ratio
		self.size = w, h



	# POSITION

	@property
	def x(self):
		cx = self.center[0]
		w = self.size[0]
		return cx - (w/2)
	@x.setter
	def x(self, arg):
		x = self.x
		self.move(arg-x, 0)

	@property
	def y(self):
		cy = self.center[1]
		h = self.size[1]
		return cy - (h/2)
	@y.setter
	def y(self, arg):
		y = self.y
		self.move(0, arg-y)


	@property
	def w(self): return self.size.x
	@property
	def h(self): return self.size.y

the_window.view = MyCamera()