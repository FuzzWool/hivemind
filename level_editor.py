import modules as mo
import modules.pysfml_game.key as key
import modules.level_editor as le

mouse = mo.MyMouse()

Camera = mo.MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = -50, 0

LevelEditor = le.LevelEditor(Camera)
#########################################################
running = True
while running:

	#Logic
	if mo.quit(): running = False

	LevelEditor.camera_controls(key, Camera)
	LevelEditor.handle_controls(key, mouse, Camera)

	#Video
	mo.window.view = Camera
	LevelEditor.Camera = Camera
	mo.window.clear(mo.sf.Color(128, 128, 128))
	#
	LevelEditor.draw(mouse, Camera)
	mo.window.view = mo.window.default_view
	LevelEditor.ToolBox.UI.draw()
	#
	mo.window.display()