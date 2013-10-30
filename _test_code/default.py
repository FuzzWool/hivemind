from code.pysfml_game import quit, window, key, sf
#########################################################
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed(): pass
	key.reset_all()


	#Video
	window.view = Camera
	window.clear(sf.Color(255,200,200))
	window.display()