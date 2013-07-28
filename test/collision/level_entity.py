from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

from modules.game import Entity
Nut = Entity("nobody")
Zachs = []
for i in range(1):
	Zach = Entity("nobody2")
	Zachs.append(Zach)
#####

from modules.game import Level
level = Level("aa", 0, 0)
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#WIP###
	amt = 5
	if key.A.held(): Nut.move(-amt, 0)
	if key.D.held(): Nut.move(+amt, 0)
	if key.W.held(): Nut.move(0, -amt)
	if key.S.held(): Nut.move(0, +amt)


	#Collision

	# for point in level.collision.points:
	# 	Nut.collision_pushback(*point)

	for Zach in Zachs:
		Nut.collision_pushback(Zach)
	# ##

	level.load_around(*Camera.tile_points)

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	# level.draw()
	Zach.draw()####
	Nut.draw()#####
	#
	window.display()