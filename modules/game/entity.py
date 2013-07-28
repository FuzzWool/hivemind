from modules.pysfml_game import sf
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
		# self.cbox.draw()

#	MOVEMENT

	def move(self, x=0, y=0):
		self.cbox.move(x, y)


#COLLISION
#Simply forwards to cboxes.
#Handles points and other Entities.

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
