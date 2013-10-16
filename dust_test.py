from code.pysfml_game import quit, window, key, sf
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0
#########################################################

from code.pysfml_game import particle_generator
pg = particle_generator()

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pg.create(amt=3, area=(100,100,120,120))

	key.reset_all()


	#Video
	window.clear(sf.Color(255,200,200))
	window.view = Camera
	pg.draw()
	window.display()