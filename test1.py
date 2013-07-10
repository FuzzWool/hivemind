import modules as mo
import modules.pysfml_game.key as key
import modules.level_editor as le

mouse = le.EditMouse()

Camera = le.RoomCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

Level = mo.Level("0")
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
	
	elif key.L_SHIFT.held():
		#Move Camera - Snap to Room
		if key.A.pressed(): Camera.room_x -= 1
		if key.D.pressed(): Camera.room_x += 1
		if key.W.pressed(): Camera.room_y -= 1
		if key.S.pressed(): Camera.room_y += 1

	else:
		#Select Tiles
		if mouse.left.held():
			LevelEditor.place_tile()
		if mouse.right.pressed():
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
			print Camera.x, mo.ROOM_WIDTH
			print Camera.room_x

	mo.window.view = Camera
	LevelEditor.Camera = Camera

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color(128, 128, 128))
	#
	LevelEditor.Grid.draw()
	Level.draw()
	LevelEditor.draw()
	#
	mo.window.display()