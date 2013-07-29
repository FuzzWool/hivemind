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
		amt = 5
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
	#Handles pushback and states in response to platforms.
		for point in collision_points:

			self.collision_pushback(*point)

			if self.cbox.collision.bottom_to_top(*point):
				self.yVel = 0
				self.can_jump = True

			if self.cbox.collision.top_to_bottom(*point):
				self.yVel = 0
				self.can_jump = False


Nut = WIPEntity("nut")

from modules.game import WorldMap
worldmap = WorldMap()
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

	# Nut.can_jump = False
	# for x in worldmap.Rooms:
	# 	for y in x:
	# 		if y != None:
	# 			Nut.handle_platforms(y.collision.points)
	####

	#Video

	Camera.center = Nut.cbox.center
	worldmap.load_around(Camera.room_points, Camera.tile_points)
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	Nut.draw()
	#
	window.display()