from window import sf
from window import window as the_window
from window import SCREEN_HEIGHT, SCREEN_WIDTH

from window import ROOM_WIDTH, ROOM_HEIGHT


class MyCamera(sf.View):
	_zoom = float(1)

	#Default settings.
	#2:1 scale
	def __init__(self):
		sf.View.__init__(self)
		self.zoom = float(2)
		self.center = the_window.view.center

	@property
	def x(self):
		cx = self.center[0]
		w = self.width
		return cx - (w/2)
	@x.setter
	def x(self, arg):
		x = self.x
		self.move(arg-x, 0)

	@property
	def y(self):
		cy = self.center[1]
		h = self.height
		return cy - (h/2)
	@y.setter
	def y(self, arg):
		y = self.y
		self.move(0, arg-y)

	#How zoomed in the level the camera is.
	@property
	def zoom(self): return self._zoom
	@zoom.setter
	def zoom(self, ratio):
		self._zoom = float(ratio)
		#
		w, h = SCREEN_WIDTH, SCREEN_HEIGHT
		w /= ratio; h /= ratio
		self.size = w, h

	#

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

the_window.view = MyCamera()