from code.pysfml_game import quit, window, key, sf
#########################################################
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

##############################
from code.game import Timer
timer = Timer()


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		if timer.stopped: timer.start()
		elif timer.started: timer.stop()
	

	key.reset_all()


	#Video
	window.view = Camera
	window.clear(sf.Color(255,200,200))
	
	timer.draw()
	
	window.display()
