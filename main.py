import modules as mo
rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)

Level = mo.Level("0")
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
	mo.window.clear(mo.sf.Color(255, 0, 255))
	#
	Level.draw()
	#
	mo.window.display()