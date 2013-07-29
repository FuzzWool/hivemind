from modules.pysfml_game import sf
from modules.pysfml_game import MySprite
from modules.pysfml_game import RENDER_CENTER
from modules.pysfml_game import GRID


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

		#Loading configuration settings.
		#Load move x, y
		#! Load clipping w, h
		filename = "sheet_config.txt"
		try:
			f = open(self.folder_dir+filename).read()
			f = f.split("\n")
			
			#Move
			x, y = f[0][6:].split(",")
			x, y = int(x), int(y)

			#Clip
			w, h = f[1][6:].split(",")
			w, h = int(w), int(h)

		except:
			f = open(self.folder_dir+filename, "w")
			f.write("Move: 0,0\nClip: 0,0")
			f.close()
			x, y = 0, 0
			w, h = 0, 0

		self.sprite.move(x, y)
		self.sprite.clip(w, h)

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
			self.x_slowdown(amt)


		if key.Z.pressed(): self.jump()


	def jump(self):
	#Jumps if the entity is able to.
		if self.can_jump: self.yVel -= 8

#	COLLISIONS

	#Forwards to cboxes.
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
	#

	def handle_platforms(self, collision):
	#Handles pushback and states in response to platforms.
	#State handling performed here.

		#Get the range to perform collision checks.
		x1, y1, x2, y2 = self.cbox.points
		x1 = int(x1/GRID)-2; y1 = int(y1/GRID)-2
		x2 = int(x2/GRID)+2; y2 = int(y2/GRID)+2
		points = collision.points_range(x1, y1, x2, y2)
		#
		for point in points:

			self.collision_pushback(*point)

			if self.cbox.collision.bottom_to_top(*point):
				self.yVel = 0
				self.can_jump = True
				self.in_air = False

			if self.cbox.collision.top_to_bottom(*point):
				if self.yVel < 0: self.yVel = 0
				self.can_jump = False

			if self.cbox.collision.left_to_right(*point)\
			or self.cbox.collision.right_to_left(*point):
				self.xVel = 0

#	STATES

	can_jump = False
	in_air = True

	@property
	def falling(self): return bool(self.yVel > 0)
	@property
	def rising(self): return bool(self.yVel < 0)