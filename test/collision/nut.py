from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0


from modules.game import Entity
class WIPEntity(Entity):

	xVel, yVel = 0, 0	
	def handle_physics(self):
		self.yVel += 0.8

		self.move(0, self.yVel)


Nut = WIPEntity("nut")

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
	amt = 3
	if key.A.held(): Nut.move(-amt, 0)
	if key.D.held(): Nut.move(+amt, 0)
	# if key.W.held(): Nut.move(0, -amt)
	# if key.S.held(): Nut.move(0, +amt)
	if key.W.pressed(): Nut.yVel -= 10

	Nut.handle_physics()

	for point in level.collision.points:
		Nut.collision_pushback(*point)

	####

	level.load_around(*Camera.tile_points)

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	level.draw()
	Nut.draw()#####
	#
	window.display()