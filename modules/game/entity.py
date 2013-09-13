from modules.pysfml_game import sf
from modules.pysfml_game import MySprite
from modules.pysfml_game import RENDER_CENTER
from modules.pysfml_game import GRID


class Entity(object):
#Stuff the Player, NPCS and enemies all have in common.

# Is loaded from a CHARACTER FILE.
# Handles COLLISIONS against the WORLD.
# WIP - Contains VALUES for MOVEMENT.

	name = None
	folder_dir = None


	#	SPRITE LOADING
	#Initializes graphics and collisions.

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
	#Loaded from a character folder.

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
		self.sprite.draw()
		# self.cbox.draw()


#	MOVEMENT
#Game physics.

	xVel, yVel = 0, 0
	xLim, yLim = 8, 8
	gravity = 0.5


	def handle_physics(self):
	#Gravity and Vel movements.
		self.cbox.collision\
		.next.store_move(self.xVel, self.yVel)

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


#	COLLISIONS
# Performs pushback and state handling.

	def reset_states(self):
		self.in_air = True
		self.can_jump = False


	def collide_with_WorldMap(self, WorldMap):
	#Checks every room inside of the WorldMap.

		self.reset_states()
		for x in WorldMap.Rooms:
			for y in x:
				if y != None:
					self.collide_with_Room(y, True)


	def collide_with_Room(self, Room,
						  called_directly=False):
	#Handles pushback and states in response to platforms.
	#State handling performed here.
		if not called_directly: self.reset_states()

		collision = Room.collision

		#Get the RANGE of checking.
		x1, y1, x2, y2 = self.cbox.points
		coat = 1
		x1 = int(round(x1/GRID))-coat;
		y1 = int(round(y1/GRID))-coat
		x2 = int(round(x2/GRID))+coat;
		y2 = int(round(y2/GRID))+coat
		x1 -= Room.x; x2 -= Room.x
		y1 -= Room.y; y2 -= Room.y


		#FIX the range
		def fix_x(x):
			if x < 0: x = 0
			if x > Room.w: x = Room.w
			return x

		def fix_y(y):
			if y < 0: y = 0
			if y > Room.h: y = Room.h
			return y

		x1, x2 = fix_x(x1), fix_x(x2)
		y1, y2 = fix_y(y1), fix_y(y2)


		##########

		#	PRUNING
		# From the range, select only the usable
		# collisions.

		###debug
		#Any tile not in range is transparent.
		for x in range(Room.w):
			for y in range(Room.h):
				sprite = Room.tiles[x][y].sprite
				if sprite.texture != None:
					sprite.color = sf.Color(255,255,255,100)


		#Look for the closest x and y tiles in the range.
		x_tile, y_tile = None, None
		for x in range(x1, x2):
			for y in range(y1, y2):

				tile = Room.tiles[x][y]
				if tile.collision != "__":
					if x_tile == None: x_tile = tile
					if y_tile == None: y_tile = tile

					new_x = tile.sprite.overlap.x(self.cbox, slope=False)
					new_y = tile.sprite.overlap.y(self.cbox, slope=False)
					x_x =  x_tile.sprite.overlap.x(self.cbox, slope=False)
					x_y =  x_tile.sprite.overlap.y(self.cbox, slope=False)
					y_x =  y_tile.sprite.overlap.x(self.cbox, slope=False)
					y_y =  y_tile.sprite.overlap.y(self.cbox, slope=False)

					if new_y >= x_y:
						if new_y > x_y: x_tile = tile
						if new_x > x_x: x_tile = tile

					if new_x >= y_x:
						if new_x > y_x: y_tile = tile
						if new_y >= y_y: y_tile = tile
		#Fixes.
		if x_tile and y_tile:
			if y_tile.y == x_tile.y: y_tile = None
			elif x_tile.x == y_tile.x: x_tile = None
		#

		# EXTRA TILES
		#2-tile slopes need extra checks for their
		#connectors.

		extra_tile1 = None; extra_tile2 = None
		extra_tile3 = None; extra_tile4 = None
		if x_tile != None:
			if x_tile.is_slope():
				x, y = x_tile.x, x_tile.y

				if x+1 < Room.w:
					extra_tile1 = Room.tiles[x+1][y]
					if extra_tile1.is_slope() == False:
						extra_tile1 = None

				if x-1 >= 0:
					extra_tile2 = Room.tiles[x-1][y]
					if extra_tile2.is_slope() == False:
						extra_tile2 = None
				
				if y+1 < Room.h:
					extra_tile3 = Room.tiles[x][y+1]
					if extra_tile3.is_slope() == False:
						extra_tile3 = None
				
				if y-1 >= 0:
					extra_tile4 = Room.tiles[x][y-1]
					if extra_tile4.is_slope() == False:
						extra_tile4 = None

		collidable_tiles = \
		[x_tile, y_tile,\
		extra_tile1, extra_tile2, extra_tile3, extra_tile4]
		collidable_tiles[:] = \
		[tile for tile in collidable_tiles if tile != None]

		##########

		# PRE-COLLISION STATES

		for tile in collidable_tiles:

			#Slope Lock
			if tile.collision not in ["__", "aa"]:
				
				#Slope lock
				t = tile.sprite
				c = self.cbox
				if c.slope_collision.bottom_to_top(t):
					
					if t.slope_collision.anchor_y == "d":

						tx = c.collision.next.x_move
						y = c.slope_collision.y_overlap_amt(t)

						if t.slope_collision.anchor_x == "l":
							if tx > 0:
								c.collision.next.y_move \
								= abs(tx)
						#
						if t.slope_collision.anchor_x == "r":
							if tx < 0:
								c.collision.next.y_move \
								= abs(tx)

		# PUSHBACK
		for tile in collidable_tiles:

			s = tile.sprite
			if tile.collision == "aa":
				self.cbox.collision.pushback(s)

			elif tile.collision != "__":
				self.cbox.slope_collision.pushback(s)

		self.cbox.collision.next.confirm_move()


		# POST-COLLISION STATES
		for tile in collidable_tiles:

			###DEBUG
			tile.sprite.color = sf.Color(255,255,255)
			###

			s = tile.sprite

			if tile.collision == "aa":
				collision = self.cbox.collision
			elif tile.collision != "__":
				collision = self.cbox.slope_collision


			if collision.bottom_to_top(s):
				if self.yVel > 0: self.yVel = 0
				self.can_jump = True
				self.in_air = False

			if collision.top_to_bottom(s):
				if self.yVel < 0: self.yVel = 0

			if tile.collision == "aa":
				if collision.left_to_right(s)\
				or collision.right_to_left(s):
					self.xVel = 0

			else:
				if collision.left_to_right(s)\
				and s.slope_collision.anchor_x=="l":
					self.xVel = 0

				if collision.right_to_left(s)\
				and s.slope_collision.anchor_x=="r":
					self.xVel = 0

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

	#	CONTROLS

	def handle_controls(self, key):
	#Keyboard controls for the player character.
		self.walk(key.LEFT, key.RIGHT)
		self.jump(key.Z)


	def jump(self, jump_key):
		if jump_key.pressed():
			if self.can_jump: self.yVel -= 8

	def walk(self, left_key, right_key):
		amt = 0.5
		walkLim = 3
		if left_key.held() or right_key.held():

			if left_key.held():
				self.facing_left = True
				if -walkLim <= self.xVel - amt:
					self.move(-amt, 0)
				self.right_slowdown(amt)

			if right_key.held():
				self.facing_right = True
				if self.xVel + amt <= walkLim:
					self.move(+amt, 0)
				self.left_slowdown(amt)

		else:
			self.x_slowdown(amt)


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