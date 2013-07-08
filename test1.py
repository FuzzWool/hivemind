import modules as mo
import modules.level_editor as le

ctrl = mo.KeyTracker(mo.sf.Keyboard.L_CONTROL)
s = mo.KeyTracker(mo.sf.Keyboard.S)
mouse = le.EditMouse()

Level = mo.Level("full")
grid = le.make_grid()
LevelEditor = le.LevelEditor(mouse, Level)
#########################################################
running = True
while running:

	#Logic
	if mo.quit(): running = False

	if ctrl.held():

		if s.pressed():
			Level.save()
		if mouse.left.pressed():
			LevelEditor.TileSelector.open()
			
	else:
		if mouse.left.held():
			LevelEditor.place_tile()
		if mouse.right.held():
			LevelEditor.remove_tile()

		if mouse.left.pressed():
			LevelEditor.TileSelector.select()
		if mouse.left.released():
			LevelEditor.TileSelector.close()

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