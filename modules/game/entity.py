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
		coat = 1
		x1 = int(round(x1/GRID))-coat;
		y1 = int(round(y1/GRID))-coat
		x2 = int(round(x2/GRID))+coat;
		y2 = int(round(y2/GRID))+coat

		#Fix the range
		x1 -= Room.x; x2 -= Room.x
		y1 -= Room.y; y2 -= Room.y
		if x1 < 0: x1 = 0
		if y1 < 0: y1 = 0
		if x2 > Room.w: x2 = Room.w
		if y2 > Room.h: y2 = Room.h

		#CHANGE THIS.
		if Room.name != "aa": return 

		#Scan the range

		##########
		#ZERO - pruning

		#Find the closest collidable tile which the
		#based on width and height area.
		c = self.cbox.center
		tx = self.cbox.collision.tx
		ty = self.cbox.collision.ty
		cx, cy = c[0]+tx, c[1]+ty
		cx = int((cx/GRID));
		cy = int((cy/GRID))

		#wip
		lx, rx = self.cbox.x1 + tx, self.cbox.x2 + tx
		lx, rx = int(lx/GRID), int(rx/GRID)
		uy, dy = self.cbox.y1 + ty, self.cbox.y2 + ty
		uy, dy = int(uy/GRID), int(dy/GRID)
		#

		###debug
		#Any tile not in range is transparent.
		for x in range(Room.w):
			for y in range(Room.h):
				sprite = Room.tiles[x][y].sprite
				if sprite.texture != None:
					sprite.color = sf.Color(255,255,255,100)

		x_tile, y_tile = None, None

		if tx <= 0: left, right = True, False
		if tx >  0: left, right = False, True
		if ty <= 0: up, down = True, False
		if ty >  0: up, down = False, True
		

		#Look for the closest x and y tiles in the range.
		x_tile, y_tile = None, None
		for x in range(x1, x2):
			for y in range(y1, y2):
				
				tile = Room.tiles[x][y]
				if tile.collision != "__":
					if x_tile == None: x_tile = tile
					if y_tile == None: y_tile = tile

					new_x = tile.sprite.overlap.x(self.cbox)
					new_y = tile.sprite.overlap.y(self.cbox)
					x_x =  x_tile.sprite.overlap.x(self.cbox)
					x_y =  x_tile.sprite.overlap.y(self.cbox)
					y_x =  y_tile.sprite.overlap.x(self.cbox)
					y_y =  y_tile.sprite.overlap.y(self.cbox)
					
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

		#For 2-tile slopes
		extra_tile = None
		if x_tile != None:
			if x_tile.collision == "da":
				x, y = x_tile.x, x_tile.y
				extra_tile = Room.tiles[x+1][y]
		#

		collidable_tiles = [x_tile, y_tile, extra_tile]
		collidable_tiles[:] = \
		[tile for tile in collidable_tiles if tile != None]
		

		# #debug
		for tile in collidable_tiles:
			tile.sprite.color = sf.Color(255,255,255,255)
		#


		# for tile in collidable_tiles:
		# 	if tile.collision not in ["__","aa"]:
		# 		tile.sprite.slope_collision.draw()

		##########

		coll = self.cbox.collision

		# Pre-collision states
		for tile in collidable_tiles:
			tile.color = sf.Color(255,255,255,255)
			if tile.collision not in ["__", "aa"]:
				
				#Slope lock
				t = tile.sprite
				c = self.cbox
				if c.slope_collision.bottom_to_top(t):
					tx = c.collision.tx

					if t.slope_collision.anchor_x == "l":
						if tx > 0: c.collision.ty = tx
					#
					if t.slope_collision.anchor_x == "r":
						if tx < 0: c.collision.ty = -tx


		#FIRST - for pushback
		for tile in collidable_tiles:

				s = tile.sprite
				if tile.collision == "aa":
					self.cbox.collision.pushback(s)

				elif tile.collision != "__":
					self.cbox.slope_collision.pushback(s)

		self.cbox.collision.confirm_move()

		#SECOND - for states
		for tile in collidable_tiles:

				if tile.collision == "aa":

					s = tile.sprite
					points = s.points

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
				elif tile.collision != "__":

					s = tile.sprite
					points = s.points

					collision = self.cbox.slope_collision
					if collision.bottom_to_top(s):
						self.yVel = 0
						self.can_jump = True
						self.in_air = False


					if collision.top_to_bottom(s):
						if self.yVel < 0: self.yVel = 0
						self.can_jump = False

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