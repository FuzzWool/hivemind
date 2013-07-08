import sfml as sf
import window as wi
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

		self.left = Button()
		self.left.held = \
		 new.instancemethod(left_held, self.left, None)

		self.right = Button()
		self.right.held = \
		 new.instancemethod(right_held, self.right, None)

	def position(self):
		return sf.Mouse.get_position(wi.window)

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

#

#Tracks whether or not a key is pressed, held, and the intervals it is held for.
class KeyTracker:
	def __init__ (self, key):
		self.key = key
		self.was_pressed = False

		self.timer = sf.Clock()
		self.secs_interval = 0
		self.intervals = 0
		self.old_secs_interval = self.secs_interval

	#Basic Events
	
	def held(self): return sf.Keyboard.is_key_pressed(self.key)

	def pressed(self):
		pressed = False
		if not self.was_pressed and self.held(): pressed = True
		else: pressed = False

		self.was_pressed = self.held()
		return pressed

	#Time-based Events

	def hit_interval(self):
		if self.timer.elapsed_time.as_seconds() >= self.secs_interval:
			self.intervals += 1
			self.timer.restart(); return True
		return False

	def decrease_interval(self):
		if self.held() \
		and self.intervals >= 10 and self.secs_interval >= 0.01:
			self.secs_interval *= 0.50; self.intervals = 0

	def set_interval(self, interval): self.secs_interval = interval; self.old_secs_interval = interval
	def reset_interval(self): self.secs_interval = self.old_secs_interval

	def intervally_held(self):
		if self.pressed(): self.timer.restart(); return True
		if self.hit_interval() and self.held(): self.decrease_interval(); return True
		if self.held() == False: self.reset_interval()
		else: return False