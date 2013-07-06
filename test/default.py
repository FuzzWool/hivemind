import modules as mo
rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)

#########################################################

running = True
while running:
	#Logic
	if mo.quit(): running = False
	if rtrn.pressed():
		pass

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#

	#
	mo.window.display()