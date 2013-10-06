from code.pysfml_game import sf
from code.pysfml_game import MySprite
from code.pysfml_game import RENDER_CENTER
from code.pysfml_game import GRID


class Entity(object):
#Stuff the Player, NPCS and enemies all have in common.

	name = None
	folder_dir = None

	#	SPRITE LOADING
	#Initializes graphics and collisions.

	def __init__ (self, name="nobody"):
		#Location
		self.name = name
		char_dir = "assets/characters/"
		self.folder_dir = char_dir + self.name + "/"
		self.make_sprite()
		self.make_cbox()

		self.reset_states()

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

		self.sprite.move((x, y))
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
		self.cbox.draw()
		self.sprite.draw()


#	COLLISIONS
# Performs pushback and state handling.

	def collide_with_WorldMap(self, WorldMap):
		
		self.reset_states()
		# collision = Room.collision

		#Get the RANGE of checking.
		x1, y1, x2, y2 = self.cbox.points
		coat = 1
		x1 = int(round(x1/GRID))-coat;
		y1 = int(round(y1/GRID))-coat
		x2 = int(round(x2/GRID))+coat;
		y2 = int(round(y2/GRID))+coat


		#FIX the range
		def fix_x(x):
			if x < 0: x = 0
			if x > WorldMap.tiles_w: x = WorldMap.tiles_w
			return x

		def fix_y(y):
			if y < 0: y = 0
			if y > WorldMap.tiles_h: y = WorldMap.tiles_h
			return y

		x1, x2 = fix_x(x1), fix_x(x2)
		y1, y2 = fix_y(y1), fix_y(y2)


		##########

		#	PRUNING
		# From the range, select only the usable
		# collisions.


		#Look for the closest x and y tiles in the range.
		x_tile, y_tile = None, None
		for x in range(x1, x2):
			for y in range(y1, y2):

				tile = WorldMap.tiles[x][y]
				if tile.collision_data != "____":
					if x_tile == None: x_tile = tile
					if y_tile == None: y_tile = tile

					new_x = tile.collision.overlap.x(self.cbox, slope=False)
					new_y = tile.collision.overlap.y(self.cbox, slope=False)
					x_x =  x_tile.collision.overlap.x(self.cbox, slope=False)
					x_y =  x_tile.collision.overlap.y(self.cbox, slope=False)
					y_x =  y_tile.collision.overlap.x(self.cbox, slope=False)
					y_y =  y_tile.collision.overlap.y(self.cbox, slope=False)

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

		# # EXTRA TILES
		# #2-tile slopes need extra checks for their
		# #connectors.

		extra_tile1 = None; extra_tile2 = None
		extra_tile3 = None; extra_tile4 = None
		if x_tile != None:
			if x_tile.collision.is_slope:
				x, y = x_tile.tile_x, x_tile.tile_y

				if x+1 < WorldMap.tiles_w:
					extra_tile1 = WorldMap.tiles[x+1][y]
					if not extra_tile1.collision.is_slope:
						extra_tile1 = None

				if x-1 >= 0:
					extra_tile2 = WorldMap.tiles[x-1][y]
					if not extra_tile2.collision.is_slope:
						extra_tile2 = None
				
				if y+1 < WorldMap.tiles_h:
					extra_tile3 = WorldMap.tiles[x][y+1]
					if not extra_tile3.collision.is_slope:
						extra_tile3 = None
				
				if y-1 >= 0:
					extra_tile4 = WorldMap.tiles[x][y-1]
					if not extra_tile4.collision.is_slope:
						extra_tile4 = None

		collidable_tiles = \
		[x_tile, y_tile,
		extra_tile1, extra_tile2, extra_tile3, extra_tile4]
		collidable_tiles[:] = \
		[tile for tile in collidable_tiles if tile != None]




		##########

		# PRE-COLLISION STATES

		for tile in collidable_tiles:

			#Slope Lock
			if tile.collision_data not in ["____", "0000"]:
				
				#Slope lock
				c = self.cbox
				if c.slope_collision.bottom_to_top(tile):
					
					if tile.slope_collision.anchor_y == "d":

						tx = c.collision.next.x_move
						y = c.slope_collision.y_overlap_amt(tile)

						if tile.slope_collision.anchor_x == "l":
							if tx > 0:
								c.collision.next.y_move \
								= abs(y) + abs(tx)
						#
						if tile.slope_collision.anchor_x == "r":
							if tx < 0:
								c.collision.next.y_move \
								= abs(y) + abs(tx)

		# PUSHBACK
		for tile in collidable_tiles:

			if tile.collision_data == "0000":
				self.cbox.collision.pushback(tile)

			elif tile.collision_data != "____":
				self.cbox.slope_collision.pushback(tile)

		self.cbox.collision.next.confirm_move()


		# POST-COLLISION STATES
		for tile in collidable_tiles:

			if tile.collision_data == "0000":
				collision = self.cbox.collision
			elif tile.collision_data != "____":
				collision = self.cbox.slope_collision

			if tile.collision_data != "____":
				if collision.bottom_to_top(tile):
					if self.yVel > 0: self.yVel = 0
					self.in_air = False
					self.hit_top_wall = True

				if collision.top_to_bottom(tile):
					if self.yVel < 0: self.yVel = 0
					self.hit_bottom_wall = True 

				if tile.collision_data == "0000":
					if collision.left_to_right(tile):
						self.xVel = 0
						self.hit_right_wall = True

					if collision.right_to_left(tile):
						self.xVel = 0
						self.hit_left_wall = True

				else:
					if collision.left_to_right(tile)\
					and tile.slope_collision.anchor_x=="l":
						self.xVel = 0

					if collision.right_to_left(tile)\
					and tile.slope_collision.anchor_x=="r":
						self.xVel = 0


		# SPECIAL STATE CHECKS
		
		#wall-hug

		if x_tile != None:
			y1, y2 = self.cbox.tile_y1, self.cbox.tile_y2
			x = x_tile.tile_x

			for y in range(y1, y2):
				tile = WorldMap.tiles[x][y]
				if not tile.is_empty():
					o = self.cbox.collision.overlap.y(tile)
					if o > 0:
						self._overlap_side_wall_value += o

		if self._overlap_side_wall_value == self.cbox.h:
			self.overlap_side_wall = True




#	STATES

	def reset_states(self):
		self.in_air = True
		#
		self.hit_left_wall = False
		self.hit_right_wall = False
		self.hit_top_wall = False
		self.hit_bottom_wall = False

		#wall-hug
		self._overlap_side_wall_value = 0
		self.overlap_side_wall = False


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

	#	MOVEMENT
	#Game physics.

	xVel, yVel = 0, 0
	xLim, yLim = 10, 10

	gravity = 0.3
	default_gravity = gravity

	def handle_physics(self):
	#Processes movements for COLLISION.
	#Handles GRAVITY.
		self.cbox.collision\
		.next.store_move(self.xVel, self.yVel)

		self.move(0, self.gravity)


	def move(self, x=0, y=0):
	#All movements are forwarded here
	#to keep within SPEED LIMITS.

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


	#Automatically SLOWS DOWN the xVel to nothingness.
	def x_slowdown(self, amt=1):
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
	#




	#	CONTROLS

	# STATES
	walking = False
	diving = False
	clinging = False
	slide_kicking = False
	crouching = False


	# HANDLERS
	def handle_controls(self, key):

		#Flags
		left_flag = key.LEFT.held()
		right_flag = key.RIGHT.held()
		up_flag = key.UP.held() #UNUSED
		down_flag = key.DOWN.held()
		jump_flag = key.Z.pressed()
		action_flag = key.X.pressed() #UNUSED


		#Controls
		if not self.slide_kicking:
			self.jump(jump_flag)
			if not self.crouching:
				self.walk(left_flag, right_flag)

		self.dive(down_flag)

		self.slide_kick(down_flag)
		self.crouch(down_flag)
		self.crouch_walk(left_flag, right_flag)

		#Wall
		self.cling(left_flag, right_flag)
		self.wall_jump(jump_flag)



	# Control definitions
	
	def walk(self, left_flag, right_flag):

		#Effect
		self.walking = False
		amt = 0.15
		walkLim = 3

		if left_flag or right_flag:

			if left_flag:

				self.facing_left = True
				if -walkLim <= self.xVel - amt:
					self.move(-amt, 0)
				self.right_slowdown(amt)


			if right_flag:
				
				self.facing_right = True
				if self.xVel + amt <= walkLim:
					self.move(+amt, 0)
				self.left_slowdown(amt)

		elif not self.in_air:
			self.x_slowdown()


	def jump(self, jump_flag):

		#Effect
		if jump_flag:
			if self.hit_top_wall: self.yVel = -5.5


	def dive(self, dive_flag):


		#Stop
		was_diving = self.diving
		self.diving = False
		
		#Start
		if self.in_air and dive_flag: self.diving = True
		
		#Effect
		if self.diving: self.move(y= +1)



	def slide_kick(self, down_flag):

		#Stop
		was_slide_kicking = self.slide_kicking
		if self.xVel == 0: self.slide_kicking = False

		#Start
		if down_flag and self.moving:
			if not self.in_air:
				if not self.crouching:
					self.slide_kicking = True

		#Effect (2)

			#Increase SPEED.
		if self.slide_kicking and not was_slide_kicking:
			if self.facing_left:  self.move(x= -4)
			if self.facing_right: self.move(x= +4)

			#Use a DECAYED SLOWDOWN.
		if self.slide_kicking:
			if not self.in_air:
				self.x_slowdown(0.25)


	def crouch(self, down_flag):

		#Stop
		was_crouching = self.crouching
		self.crouching = False

		#Start
		if self.slide_kicking: return
		if down_flag and not self.in_air:
			self.crouching = True

		#Effect
		if self.crouching and not was_crouching:
			self.xVel = 0
	
	#
	def crouch_walk(self, left_flag, right_flag):

		#Effect
		if self.crouching:
			
			speed, limit = 1, 1

			#! Crudely COPY AND PASTED from walk.
			if left_flag:	
				self.facing_left = True
				if -limit <= self.xVel - speed:
					self.move(-speed, 0)
				self.right_slowdown(speed)

			elif right_flag:
				self.facing_right = True
				if self.xVel + speed <= limit:
					self.move(+speed, 0)
				self.left_slowdown(speed)
			#
			else:
				self.x_slowdown()



	#Wall

	def cling(self, left_flag, right_flag):

		#Stop
		was_clinging = self.clinging
		self.clinging = False
		if self.diving == False:
			self.gravity = self.default_gravity

		#Start
		if self.in_air and self.overlap_side_wall:
			if self.hit_right_wall and self.facing_left\
			or self.hit_left_wall and self.facing_right:
				self.clinging = True

		#Effect
		if self.clinging:
			if not self.diving and self.falling:
				self.gravity = 0.02
				if not was_clinging: self.yVel = 0




	def wall_jump(self, jump_flag):

		#Effect
		if self.clinging and jump_flag:
			if self.facing_left:
				self.xVel = 4.5
				self.facing_right = True
			elif self.facing_right:
				self.xVel = -4.5
				self.facing_left = True
			self.yVel = -4



	#GRAPHICS

	def draw(self):

		#Direction
		if self.facing_right:
			if self.sprite.clip.flipped:
				self.sprite.clip.flip()
		if self.facing_left:
			if not self.sprite.clip.flipped:
				self.sprite.clip.flip()

		#Jumping
		if self.in_air:
			if self.rising:
				self.sprite.clip.use(2, 0)
			if self.falling:
				self.sprite.clip.use(4, 0)

		#Walking
		else:
			if self.moving:
				sequence = ((1,1),(0,1),(3,1),(2,1))
				self.sprite.animation.clips = sequence
				self.sprite.animation.clip_interval = 0.1
			else:
				self.sprite.clip.use(0, 0)

		#Special

		if self.clinging:
			self.sprite.clip.use(0,2)

		if self.slide_kicking:
			self.sprite.clip.use(0,4)

		if self.crouching:
			if self.moving:
				sequence = []
				for i in range(6): sequence.append((i,3))
				self.sprite.animation.clips = sequence
				self.sprite.animation.clip_interval = 0.05
			else:		
				self.sprite.clip.use(0,3)



		#Drawing
		Entity.draw(self)

	def play(self):
		self.sprite.animation.play()