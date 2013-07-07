import modules as mo
import modules.level_editor as le
# rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)
ctrl = mo.KeyTracker(mo.sf.Keyboard.L_CONTROL)
s = mo.KeyTracker(mo.sf.Keyboard.S)
mouse = mo.MyMouse()

Level = mo.Level("full")
grid = le.make_grid()
LevelEditor = le.LevelEditor(Level)
#########################################################
running = True
while running:

	#Logic
	if mo.quit(): running = False

	if ctrl.held():
		if s.pressed():
			Level.save()
	else:
		if mouse.left.held():
			LevelEditor.place_tile(*mouse.position())
		if mouse.right.held():
			LevelEditor.remove_tile(*mouse.position())

	LevelEditor.loop()

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#
	for g in grid:
		g.draw()
	Level.draw()
	LevelEditor.draw()
	#
	mo.window.display()