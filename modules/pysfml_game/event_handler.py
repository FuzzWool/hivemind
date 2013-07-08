import sfml as sf
import window as wi
from mycamera import Camera
import new

#Quit the app.
def quit():
	window = wi.window
	for event in window.iter_events():
		if event.type == sf.Event.CLOSED:
			return True
		if event.type == sf.Event.KEY_PRESSED:
			if event.code == sf.Keyboard.ESCAPE:
				return True
	return False

#

class MyMouse:
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

	def position(self):
	#Camera offset and zoom don't impact it.
		pos = sf.Mouse.get_position(wi.window)
		x = int(pos[0]+(Camera.x*Camera.zoom))
		x = int(x/Camera.zoom)
		y = int(pos[1]+(Camera.y*Camera.zoom))
		y = int(y/Camera.zoom)
		return x, y

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

	def released(self):
		release = False
		if self.old_held2 == True:
			if self.held() == False:
				release = True
		self.old_held2 = self.held()
		return release