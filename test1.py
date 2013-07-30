from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0


from modules.game import Entity
class Player(Entity):
	#GRAPHICS

	def draw(self):

		#Direction
		if self.facing_right:
			if self.sprite.clip.flipped:
				self.sprite.clip.flip()
		if self.facing_left:
			if not self.sprite.clip.flipped:
				self.sprite.clip.flip()

		#Animation
		if self.in_air:
			if self.rising:
				self.sprite.clip.use(2, 0)
			if self.falling:
				self.sprite.clip.use(4, 0)

		else:
			if self.moving:
				sequence = ((1,1),(0,1),(3,1),(2,1))
				self.sprite.animation.clips = sequence
				self.sprite.animation.clip_interval = 0.1
			else:
				self.sprite.clip.use(0, 0)

		#Drawing
		Entity.draw(self)

	def play(self):
		self.sprite.animation.play()

Nut = Player("nut")

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

	Nut.in_air = True
	Nut.can_jump = False
	for x in worldmap.Rooms:
		for y in x:
			if y != None:
				Nut.handle_platforms(y.collision)
	###

	#Animation
	Nut.play()

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