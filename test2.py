import modules as mo
rtrn = mo.KeyTracker(mo.mo.sf.Keyboard.RETURN)

import new
#MyMouse release.
class MyMouse:
	def __init__(self):
		def left_held(self):
			return mo.sf.Mouse.is_button_pressed\
			 (mo.sf.Mouse.LEFT)

		def right_held(self):
			return mo.sf.Mouse.is_button_pressed\
			 (mo.sf.Mouse.RIGHT)

		self.left = Button()
		self.left.held = \
		 new.instancemethod(left_held, self.left, None)

		self.right = Button()
		self.right.held = \
		 new.instancemethod(right_held, self.right, None)

	def position(self):
		return mo.sf.Mouse.get_position(wi.window)

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


Mouse = MyMouse()
#########################################################

running = True
while running:
	#Logic
	if mo.quit(): running = False

	if Mouse.left.released():
		print 100

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#

	#
	mo.window.display()