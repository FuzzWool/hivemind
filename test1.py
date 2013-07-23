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

#	SPRITE LOADING
	folders_dir = "img/characters/"
	image = None
	texture = None
	sprite = None

	def __init__ (self, name="nobody"):
		#Location
		self.name = name
		folder_dir = self.folders_dir + name + "/"

		#Set the image.
		self.image = sf.Image\
		.load_from_file(folder_dir+"sheet.png")
		self.image\
		.create_mask_from_color(sf.Color(255, 0, 255))
		
		#Make the texture.
		self.texture = sf.Texture\
		.load_from_image(self.image)

		#Make the sprite.
		self.sprite = MySprite(self.texture)
		# self.sprite.clip.set(40, 40)
		# self.sprite.clip.use(0, 0)

		self.sprite.center = RENDER_CENTER

	def draw(self):
		self.sprite.draw()


#	MOVEMENT
	yVel = 0

	def movement(self):
		self.gravity()

	def gravity(self):
		self.yVel += 0.3
		self.sprite.y += self.yVel
#


#####
Nut = Entity("nut")
Zach = Entity("zach")

from modules.worldmap import WorldMap
worldmap = WorldMap()
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	worldmap.load_around\
	(Camera.room_points, Camera.tile_points)

	#WIP####
	# Nut.movement()
	####

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	Nut.draw()#####
	Zach.draw()
	#
	window.display()