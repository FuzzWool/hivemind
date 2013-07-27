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

	def move(self, x=0, y=0):
		self.cbox.move(x, y)

	yVel = 0
	def gravity(self):
		self.yVel += 0.3
		self.sprite.y += self.yVel


#	COLLISION
#Handles points and other Entities.

	### May use points or other entities.
	def is_colliding(self, x1=0, y1=0, x2=0, y2=0):
		if  type(x1) != int\
		and type(x1) != float: 
			return self.cbox.collision(x1.cbox)
		else:
			return self.cbox.collision(x1, y1, x2, y2)

	def collision_pushback(self, x1=0, y1=0, x2=0, y2=0):
		if  type(x1) != int\
		and type(x1) != float: 
			self.cbox.collision.pushback(x1.cbox)
		else:
			self.cbox.collision.pushback(x1, y1, x2, y2)
	###

#


Nut = Entity("nobody")
Zachs = []
for i in range(1):
	Zach = Entity("nobody2")
	Zachs.append(Zach)
#####

from modules.level import Level
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