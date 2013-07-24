from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

#	ENTITY
from modules.pysfml_game import MySprite
from modules.pysfml_game import RENDER_CENTER

class Entity:
#Stuff the Player, NPCS and enemies all have in common.

	name = None
	folder_dir = None

#	SPRITE LOADING

	def __init__ (self, name="nobody"):
		#Location
		self.name = name
		char_dir = "img/characters/"
		self.folder_dir = char_dir + self.name + "/"
		self.make_sprite()
		self.make_cbox()

	image = None
	texture = None
	sprite = None

	def make_sprite(self):
	#Create the main sprite.

		#Set the image.
		self.image = sf.Image\
		.load_from_file(self.folder_dir+"sheet.png")
		self.image\
		.create_mask_from_color(sf.Color(255, 0, 255))
		
		#Make the texture.
		self.texture = sf.Texture\
		.load_from_image(self.image)

		#Make the sprite.
		self.sprite = MySprite(self.texture)

	cbox_tex = None
	cbox = None

	def make_cbox(self):
		#Make the sprite.
		self.cbox_tex = sf.Texture\
		.load_from_file(self.folder_dir+"cbox.png")
		self.cbox = MySprite(self.cbox_tex)

		#Parents all the other sprites.
		self.cbox.children.append(self.sprite)

		self.cbox.center = RENDER_CENTER


	def draw(self):
		self.sprite.draw()
		self.cbox.draw()


#	MOVEMENT
#Collisions use cbox.

	###WIP###
	def move(self, Entity, move=(0, 0)):
	#Process collisions for every moment.
		x, y = move
		self.cbox.move(x, y)

		ox, oy = self.collision_offset(Entity)

	def collision_offset(self, Entity):
	#Work out the offset to move by.

		a, b = self.cbox, Entity.cbox

		#Compare against B's area.
		def collision_area(x, y):
		#Return the offset.
			ox, oy = 0, 0

			if  b.x1 < x < b.x2\
			and b.y1 < y < b.y2:

				#Find the smallest way out.
				left = x - b.x1
				right = b.x2 - x
				#Return the actual movement.
				if left < right:
					ox = -left
				else:
					ox = right

				top = y - b.y1
				bottom = b.y2 - y
				if top < bottom:
					oy = -top
				else:
					oy = bottom

			return ox, oy


		#With all of A's points.
		for x in [a.x1, a.x2]:
			for y in [a.y1, a.y2]:

				#Find the biggest intersection.
				print collision_area(x, y)
		print

		#PROBLEM: Needs to account for the amount push.
		#eg, x1 to move back to a place where
		# it'd satisfy x2

		return 0, 0

	###

	yVel = 0
	def gravity(self):
		self.yVel += 0.3
		self.sprite.y += self.yVel
#


Nut = Entity("nobody")
Zach = Entity("nobody2")
#####

from modules.worldmap import WorldMap
worldmap = WorldMap()
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#WIP###
	amt = 5
	if key.A.held(): Nut.move(Zach, (-amt, 0))
	if key.D.held(): Nut.move(Zach, (+amt, 0))
	if key.W.held(): Nut.move(Zach, (0, -amt))
	if key.S.held(): Nut.move(Zach, (0, +amt))
	###

	worldmap.load_around\
	(Camera.room_points, Camera.tile_points)

	#WIP####
	# Nut.collision_pushback(Zach)
	###

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	Zach.draw()####
	Nut.draw()#####
	#
	window.display()