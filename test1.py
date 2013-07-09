import modules as mo
import modules.pysfml_game.key as key
import modules.level_editor as le

mouse = le.EditMouse()

Camera = mo.MyCamera()
Camera.x, Camera.y = 0, 0

Level = mo.Level("full")
grid = le.make_grid()
LevelEditor = le.LevelEditor(mouse, Camera, Level)

#########################################################
running = True
while running:

	#Logic
	if mo.quit(): running = False

	if key.L_CTRL.held():
		#Save Level
		if key.S.pressed():
			Level.save()

		#Open Tile Selector menu
		if mouse.left.pressed():
			LevelEditor.TileSelector.open()

		#Zoom Camera
		if key.ADD.pressed(): Camera.zoom *= 2
		if key.SUBTRACT.pressed(): Camera.zoom /= 2
			
	else:
		#Select Tiles
		if mouse.left.held():
			LevelEditor.place_tile()
		if mouse.right.held():
			LevelEditor.remove_tile()
		if mouse.left.pressed():
			LevelEditor.TileSelector.select()
		if mouse.left.released():
			LevelEditor.TileSelector.close()

		#Move Camera
		if key.A.held(): Camera.x -= mo.GRID
		if key.D.held(): Camera.x += mo.GRID
		if key.W.held(): Camera.y -= mo.GRID
		if key.S.held(): Camera.y += mo.GRID

		#Test
		if key.RETURN.pressed():
			pass

	mo.window.view = Camera
	LevelEditor.Camera = Camera

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color(128, 128, 128))
	#
	for g in grid:
		g.draw()
	Level.draw()
	LevelEditor.draw()
	#
	mo.window.display()