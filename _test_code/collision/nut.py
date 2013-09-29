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

#	PHYSICS

	gravity = 0.5
	xVel, yVel = 0, 0
	xLim, yLim = "to add", 8

	def handle_physics(self):
	#Gravity
		if self.yVel + self.gravity < self.yLim:
			self.yVel += self.gravity
		else: self.yVel = self.yLim
		self.move(0, self.yVel)


#	CONTROLS

	def handle_controls(self, key):
	#Keyboard controls for the player character.
		amt = 3
		if key.LEFT.held(): Nut.move(-amt, 0)
		if key.RIGHT.held(): Nut.move(+amt, 0)
		if key.Z.pressed():
			Nut.jump()


	can_jump = False

	def jump(self):
		if self.can_jump:
			Nut.yVel -= 8

#	COLLISIONS

	def handle_platforms(self, collision_points):
		self.can_jump = False
		for point in collision_points:

			self.collision_pushback(*point)

			if self.cbox.collision.bottom_to_top(*point):
				self.yVel = 0
				self.can_jump = True

			if self.cbox.collision.top_to_bottom(*point):
				self.yVel = 0
				self.can_jump = False


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
	Nut.handle_controls(key)
	Nut.handle_physics()
	Nut.handle_platforms(level.collision.points)
	####

	#Video

	# Camera.center = Nut.cbox.center

	level.load_around(*Camera.tile_points)
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	level.draw()
	Nut.draw()
	#
	window.display()