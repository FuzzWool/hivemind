from modules.pysfml_game import sf
from modules.pysfml_game import MySprite
from modules.pysfml_game import RENDER_CENTER
from modules.pysfml_game import GRID


class Entity(object):
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
		.from_file(self.folder_dir+"sheet.png")
		self.image\
		.create_mask_from_color(sf.Color(255, 0, 255))
		
		#Make the texture.
		self.texture = sf.Texture\
		.from_image(self.image)

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
		.from_file(self.folder_dir+"cbox.png")
		self.cbox = MySprite(self.cbox_tex)

		#Parents all the other sprites.
		self.cbox.children.append(self.sprite)

		self.cbox.center = RENDER_CENTER


	def draw(self):
		# self.sprite.draw()
		self.cbox.draw()

#	MOVEMENT

	xVel, yVel = 0, 0
	xLim, yLim = 8, 8
	gravity = 0.5

	def handle_physics(self):
	#Gravity and Vel movements.
		self.cbox.collision.try_move(self.xVel, self.yVel)

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
				self.facing_left = True
				if -walkLim <= self.xVel - amt:
					self.move(-amt, 0)
				self.right_slowdown(amt)
			
			if key.RIGHT.held():
				self.facing_right = True
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

	def collide_with_WorldMap(self, WorldMap):
	#Checks every room inside of the WorldMap.
		self.in_air = True
		self.can_jump = False

		for x in WorldMap.Rooms:
			for y in x:
				if y != None:
					self.collide_with_Room(y, True)

	def collide_with_Room(self, Room,
						  called_directly=False):
	#Handles pushback and states in response to platforms.
	#State handling performed here.
		if not called_directly:
			self.in_air = True
			self.can_jump = False

		collision = Room.collision

		#Get the range to perform collision checks.
		x1, y1, x2, y2 = self.cbox.points
		x1 = int(x1/GRID)-2; y1 = int(y1/GRID)-2
		x2 = int(x2/GRID)+2; y2 = int(y2/GRID)+2

		#Fix the range
		x1 -= Room.x; x2 -= Room.x
		y1 -= Room.y; y2 -= Room.y
		if x1 < 0: x1 = 0
		if y1 < 0: y1 = 0
		if x2 > Room.w: x2 = Room.w
		if y2 > Room.h: y2 = Room.h


		#Scan the range

		#ZERO - pruning
		x_tile, y_tile = None, None

		#Find the closest collidable tile which the
		#based on width and height area.
		c = self.cbox.center
		tx = self.cbox.collision.tx
		ty = self.cbox.collision.ty
		cx, cy = c[0]+tx, c[1]+ty
		cx = int(cx/GRID); cy = int(cy/GRID)


		#Debug

		#Any tile not in range is transparent.
		for x in range(Room.w):
			for y in range(Room.h):
				sprite = Room.tiles[x][y].sprite
				if sprite.texture != None:
					sprite.color = sf.Color(255,255,255,100)

		#Any tile in range is opaque.
		for x in range(x1, x2):
			for y in range(y1, y2):
				sprite = Room.tiles[x][y].sprite
				if sprite.texture != None:
					sprite.color = sf.Color(255,255,255,255)

		#Find the NEAREST x collision.
		#(A space which isn't empty.)
		pass

		#Find the NEAREST y collision.
		pass


		#FIRST - for pushback
		for x in range(x1, x2):
			for y in range(y1, y2):

				tile = Room.tiles[x][y].sprite
				if Room.tiles[x][y].collision == "aa":
					self.cbox.collision.pushback(tile)

				elif Room.tiles[x][y].collision != "__":
					self.cbox.slope_collision.pushback(tile)


		self.cbox.collision.confirm_move()

		#SECOND - for states
		for x in range(x1, x2):
			for y in range(y1, y2):

				if Room.tiles[x][y].collision == "aa":

					tile = Room.tiles[x][y].sprite
					points = tile.points

					collision = self.cbox.collision
					if collision.bottom_to_top(*points):
						self.yVel = 0
						self.can_jump = True
						self.in_air = False

					if collision.top_to_bottom(*points):
						if self.yVel < 0: self.yVel = 0

					if collision.left_to_right(*points)\
					or collision.right_to_left(*points):
						self.xVel = 0

				#Slope collisions
				elif Room.tiles[x][y].collision != "__":

					tile = Room.tiles[x][y].sprite
					points = tile.points

					collision = self.cbox.slope_collision
					if collision.bottom_to_top(tile):
						self.yVel = 0
						self.can_jump = True
						self.in_air = False

					if collision.top_to_bottom(tile):
						# if self.yVel < 0: self.yVel = 0
						self.can_jump = False

					# if collision.left_to_right(tile)\
					# or collision.right_to_left(tile):
					# 	self.xVel = 0

#	STATES

	can_jump = False
	in_air = True

	facing_left = False
	@property
	def facing_right(self):
		return not self.facing_left
	@facing_right.setter
	def facing_right(self, arg):
		self.facing_left = not arg

	@property
	def falling(self): return bool(self.yVel > 0)
	@property
	def rising(self): return bool(self.yVel < 0)
	@property
	def moving(self): return bool(self.xVel != 0)




class Player(Entity):
# Nut's functionality.

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