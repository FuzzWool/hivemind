import modules as mo
import new

rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)

mouse = mo.MyMouse()
#########################################################
running = True
while running:
	
	#Logic
	if mo.quit(): running = False

	if mouse.right.pressed():
		print "Click."
	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#
	#
	mo.window.display()