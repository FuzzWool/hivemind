from window import window
from window import RENDER_WIDTH, RENDER_HEIGHT
from window import SCREEN_HEIGHT, SCREEN_WIDTH
from window import SCALE

class MyCamera(object):
#Simplication of mo.window.view
	_ = window.view
	_zoom = SCALE

	@property
	def x(self):
		cx = self._.center[0]
		w = self._.width
		return cx - (w/2)
	@x.setter
	def x(self, arg):
		x = self.x
		self._.move(arg-x, 0)

	@property
	def y(self):
		cy = self._.center[1]
		h = self._.height
		return cy - (h/2)
	@y.setter
	def y(self, arg):
		y = self.y
		self._.move(0, arg-y)

	@property
	def zoom(self): return self._zoom
	@zoom.setter
	def zoom(self, ratio):
		self._zoom = float(ratio)
		#
		w, h = SCREEN_WIDTH, SCREEN_HEIGHT
		w /= ratio; h /= ratio
		self._.size = w, h

Camera = MyCamera()