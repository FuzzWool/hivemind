import sfml as sf
import window as wi
# from mycamera import Camera
import new

#Quit the app.
import key
def quit():
	window = wi.window
	for event in window.events:
		if type(event) is sf.CloseEvent: return True
		if key.ESCAPE.pressed(): return True
	return False

#

from code.pysfml_game import GRID
from code.pysfml_game import ROOM_WIDTH, ROOM_HEIGHT
from code.pysfml_game import GameRectangle

class MyMouse(GameRectangle):
	w,h = 0,0

	def __init__(self):
		def left_held(self):
			return sf.Mouse.is_button_pressed\
			 (sf.Mouse.LEFT)

		def right_held(self):
			return sf.Mouse.is_button_pressed\
			 (sf.Mouse.RIGHT)

		def middle_held(self):
			return sf.Mouse.is_button_pressed\
			 (sf.Mouse.MIDDLE)

		self.left = Button()
		self.left.held = \
		 new.instancemethod(left_held, self.left, None)

		self.right = Button()
		self.right.held = \
		 new.instancemethod(right_held, self.right, None)

		self.middle = Button()
		self.middle.held = \
		 new.instancemethod(middle_held, self.middle, None)

	@property
	def x(self): return self.position()[0]

	@property
	def y(self): return self.position()[1]

	def position(self, Camera=None):
	#Takes offsets from the Camera in to account.
		pos = sf.Mouse.get_position(wi.window)
		x, y = pos
		if Camera != None:
			x = int(pos[0]+(Camera.x*Camera.zoom))
			x = int(x/Camera.zoom)
			y = int(pos[1]+(Camera.y*Camera.zoom))
			y = int(y/Camera.zoom)
		return x, y

	#

	# def grid_position(self, Camera=None):
	# #Return the mouse position as small grid coordinates.
	# 	x, y = self.position(Camera)
	# 	x /= GRID
	# 	y /= GRID
	# 	return x, y

	# def room_position(self, Camera=None):
	# #Return the mouse as tiny room coordinates.
	# 	x, y = self.position(Camera)
	# 	x = int(x/ROOM_WIDTH)
	# 	y = int(y/ROOM_HEIGHT)
	# 	return x, y


class Button:
#Instance designed to be overriden.
#An event which notices changes to a bool.
	old_held = None
	old_held2 = None

	def held(self):
	#Override me!
		return False

	def pressed(self):
		press = False
		if self.old_held == False:
			if self.held() == True:
				press = True
		self.old_held = self.held()
		return press

	def clicked(self): return self.pressed()

	def released(self):
		release = False
		if self.old_held2 == True:
			if self.held() == False:
				release = True
		self.old_held2 = self.held()
		return release

	#

	first_press = False
	clock = sf.Clock()

	def double_pressed(self, secs=0.3):
		#If unpressed, check to see if pressed again.
		if self.first_press == False:
			self.first_press = self.pressed()
			self.clock.restart()

		#If time runs out, the first press is falsed.
		if self.first_press\
		 and self.clock.elapsed_time.seconds >= secs:
		 	self.first_press = False
		 	self.clock.restart()

		return self.pressed() and self.first_press

	def double_clicked(self, secs=0.3):
		return self.double_pressed(secs)