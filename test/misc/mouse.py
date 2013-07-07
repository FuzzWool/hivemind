import modules as mo
rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)

#held, pressed
class MyMouse:
	was_held = False

	def held(self):
		return \
		mo.sf.Mouse.is_button_pressed(mo.sf.Mouse.LEFT)

	def pressed(self):
		truth = False
		if not self.was_held:
			if self.held(): truth = True
		self.was_held = self.held()
		return truth

mouse = MyMouse()
#########################################################
running = True
while running:
	
	#Logic
	if mo.quit(): running = False
	if rtrn.pressed():
		pass

	if mouse.pressed():
		print 1

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#
	#
	mo.window.display()