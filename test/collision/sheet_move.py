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

		#Set the image (load sheet)
		self.image = sf.Image\
		.load_from_file(self.folder_dir+"sheet.png")
		self.image\
		.create_mask_from_color(sf.Color(255, 0, 255))
		
		#Make the texture.
		self.texture = sf.Texture\
		.load_from_image(self.image)

		#Make the sprite.
		self.sprite = MySprite(self.texture)

		#(load goto)
		filename = "sheet_move.txt"
		try:
			f = open(self.folder_dir+filename).read()
			x, y = f.split(",")
			x, y = int(x), int(y)
		except:
			f = open(self.folder_dir+filename, "w")
			f.write("0,0")
			f.close()
			x, y = 0, 0
		self.sprite.move(x, y)

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
	def move(self, x=0, y=0):
		self.cbox.move(x, y)

	def is_colliding(self, Entity):
		a, b = self.cbox, Entity.cbox
		if  b.x1 <= a.x1 <= b.x2\
		and b.y1 <= a.y1 <= b.y2:
			return True
		if  b.x1 <= a.x2 <= b.x2\
		and b.y1 <= a.y2 <= b.y2:
			return True
		return False

	def collision_pushback(self, Entity):
	#Check the Entity's collision against another.

		if not self.is_colliding(Entity): return

		#If so, find the offset to move.
		ox, oy = self._collision_offset(Entity)
		if abs(ox) < abs(oy): self.cbox.move(ox, 0)
		else: self.cbox.move(0, oy)

	def _collision_offset(self, Entity):
	#Work out the offset to move by.

		a, b = self.cbox, Entity.cbox

		#Compare against b's area.
		def collision_area(x, y):
		#Return the offset.
			ox, oy = 0, 0

			if  b.x1 <= x <= b.x2\
			and b.y1 <= y <= b.y2:

				#Find the shortest way out.
				#(To be side-by-side)
				#1: Positive, 2: Negative
				if x == a.x1: ox = b.x2 - x
				if x == a.x2: ox = b.x1 - x
				if y == a.y1: oy = b.y2 - y
				if y == a.y2: oy = b.y1 - y

			return ox, oy

		#With all of A's points.
		#Find the smallest offset.
		ox, oy = 0, 0
		for x in [a.x1, a.x2]:
			for y in [a.y1, a.y2]:

				#See if the way out is smaller.
				tx, ty = collision_area(x, y)
				if (ox, oy) == (0, 0):
					ox, oy = tx, ty
				if tx != 0:
					if abs(tx) < abs(ox): ox = tx
				if ty != 0:
					if abs(ty) < abs(oy): oy = ty

		return ox, oy

	###

	yVel = 0
	def gravity(self):
		self.yVel += 0.3
		self.sprite.y += self.yVel
#


Nut = Entity("nut")
Zachs = []
for i in range(1):
	Zach = Entity("zach")
	Zachs.append(Zach)
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
	if key.A.held(): Nut.move(-amt, 0)
	if key.D.held(): Nut.move(+amt, 0)
	if key.W.held(): Nut.move(0, -amt)
	if key.S.held(): Nut.move(0, +amt)

	for Zach in Zachs:
		Nut.collision_pushback(Zach)
	###

	worldmap.load_around\
	(Camera.room_points, Camera.tile_points)

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	#worldmap.draw()
	Zach.draw()####
	Nut.draw()#####
	#
	window.display()