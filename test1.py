from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0


from modules.game import Entity
from modules.pysfml_game import GRID
class WIPEntity(Entity):

#	PHYSICS

	xVel, yVel = 0, 0
	xLim, yLim = 8, 8
	gravity = 0.5

	def handle_physics(self):
	#Gravity and Vel movements.
		self.cbox.move(self.xVel, self.yVel)

		#Gravity
		self.move(0, self.gravity)

	def move(self, x=0, y=0):
	#Doesn't move directly. Impacts the Vel.
	#Needs physics to be handled.

		#Speed limits. Cannot ever be exceeded.
		if   self.xVel + x > +self.xLim:
			self.xVel = self.xLim
		elif self.xVel + x < -self.xLim:
			self.xVel = -self.xLim
		else:
			self.xVel += x

		if   self.yVel + y > +self.yLim:
			self.yVel = self.yLim
		elif self.yVel + y < -self.yLim:
			self.yVel = -self.yLim
		else:
			self.yVel += y


	def x_slowdown(self, amt=1):
	#Slowdown the xVel to nothingness.
		self.right_slowdown(amt)
		self.left_slowdown(amt)
		#
	def right_slowdown(self, amt=1):
		if self.xVel > 0:
			if self.xVel - amt < 0: self.xVel = 0
			else: self.xVel -= amt
		#
	def left_slowdown(self, amt=1):
		if self.xVel < 0:
			if self.xVel + amt > 0: self.xVel = 0
			else: self.xVel += amt


#	CONTROLS

	def handle_controls(self, key):
	#Keyboard controls for the player character.

		amt = 0.5
		walkLim = 3 #Walking speed limit.
		if key.LEFT.held() or key.RIGHT.held():
			
			if key.LEFT.held():
				if -walkLim <= self.xVel - amt:
					self.move(-amt, 0)
				self.right_slowdown(amt)
			
			if key.RIGHT.held():
				if self.xVel + amt <= walkLim:
					self.move(+amt, 0)
				self.left_slowdown(amt)

		else:
			self.x_slowdown()


		if key.Z.pressed(): self.jump()


	can_jump = False
	def jump(self):
	#Jumps if the entity is able to.
		if self.can_jump: self.yVel -= 8

#	COLLISIONS

	def handle_platforms(self, collision):
	#Handles pushback and states in response to platforms.
		#Get the range to perform collision checks.
		x1, y1, x2, y2 = Nut.cbox.points
		x1 = int(x1/GRID)-2; y1 = int(y1/GRID)-2
		x2 = int(x2/GRID)+2; y2 = int(y2/GRID)+2
		points = collision.points_range(x1, y1, x2, y2)
		#

		for point in points:

			self.collision_pushback(*point)

			if self.cbox.collision.bottom_to_top(*point):
				self.yVel = 0
				self.can_jump = True

			if self.cbox.collision.top_to_bottom(*point):
				if self.yVel < 0: self.yVel = 0
				self.can_jump = False

			if self.cbox.collision.left_to_right(*point)\
			or self.cbox.collision.right_to_left(*point):
				self.xVel = 0


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

	Nut.can_jump = False
	for x in worldmap.Rooms:
		for y in x:
			if y != None:
				Nut.handle_platforms(y.collision)
	###

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