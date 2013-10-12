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



		#Sub-classes
		self.physics = physics()
		self.collision = collision()
		self.controls = controls()

		s=self
		s.physics.bind(s.cbox)
		s.collision.bind(s.controls, s.physics, s.cbox)
		s.controls.bind(s.physics, s.collision, s.cbox)



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

		self.default_sprite_move = (x, y)
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
		# self.cbox.draw()
		
		self.controls.change_sprite\
		(self.sprite, self.cbox, self.default_sprite_move)
		self.sprite.animation.play()
		self.sprite.draw()




######################
######################
######################
######################
######################



class collision:
# The entity's collision against the WorldMap.
# Handles pushback, provides states.


	def bind(self, controls, physics, cbox): #init
		self.controls = controls
		self.physics = physics
		self.cbox = cbox
		#
		self.reset_states()

	def __call__(self, WorldMap):
		
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
		# #Fixes.
		# if x_tile and y_tile:
		# 	if y_tile.y == x_tile.y: y_tile = None
		# 	elif x_tile.x == y_tile.x: x_tile = None
		# #

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
					if self.physics.yVel > 0: self.physics.yVel = 0
					self.in_air = False
					self.hit_top_wall = True

				if collision.top_to_bottom(tile):
					if self.physics.yVel < 0: self.physics.yVel = 0
					self.hit_bottom_wall = True 

				if tile.collision_data == "0000":
					if collision.left_to_right(tile):
						self.physics.xVel = 0
						self.hit_right_wall = True

					if collision.right_to_left(tile):
						self.physics.xVel = 0
						self.hit_left_wall = True

				else:
					if collision.left_to_right(tile)\
					and tile.slope_collision.anchor_x=="l":
						self.physics.xVel = 0

					if collision.right_to_left(tile)\
					and tile.slope_collision.anchor_x=="r":
						self.physics.xVel = 0




		# SPECIAL STATE CHECKS

		
		#wall hug
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


		#wall hang
		if x_tile != None:
			x, y = x_tile.tile_position
			tile_above = WorldMap.tiles[x][y-1]
			tile = WorldMap.tiles[x][y]

			if not tile.is_empty() \
			and tile_above.is_empty():

				old_y1=self.cbox.collision.previous.y1
				new_y1=self.cbox.y1
				tile_y1=tile.y1

				if old_y1 < tile_y1 < new_y1:
					self.top_passed_top_wall = True
					self._top_passed_tile_y1 = tile_y1


		#crawling > wall hang

		if y_tile != None:
			
			next = None
			x, y = y_tile.tile_position
			if self.controls.facing_left:
				if WorldMap.in_range(x-1, y):
					next = WorldMap.tiles[x-1][y]
			if self.controls.facing_right:
				if WorldMap.in_range(x+1, y):
					next = WorldMap.tiles[x+1][y]

			if next != None:
				if next.is_empty():

					if self.controls.facing_left:
						if self.cbox.x1 < y_tile.x1:
							self.left_passes_left_wall\
							=True
							self._left_passes_tile_x1\
							= y_tile.x1

							self._side_passes_tile_y1\
							= y_tile.y1

					if self.controls.facing_right:
						if self.cbox.x2 > y_tile.x2:
							self.right_passes_right_wall\
							=True
							self._right_passes_tile_x2\
							= y_tile.x2

							self._side_passes_tile_y1\
							= y_tile.y1


#	STATES

	def reset_states(self):
		self.in_air = True
		#
		self.hit_left_wall = False
		self.hit_right_wall = False
		self.hit_top_wall = False
		self.hit_bottom_wall = False

		#wall hug
		self._overlap_side_wall_value = 0
		self.overlap_side_wall = False

		#wall hang
		self.top_passed_top_wall = False
		self._top_passed_tile_y1 = 0

		#crawling > wall hang
		self.left_passes_left_wall = False
		self.right_passes_right_wall = False
		self._left_passes_tile_x1 = 0
		self._right_passes_tile_x2 = 0
		self._side_passes_tile_y1 = 0


	@property
	def hit_side_wall(self):
		if self.hit_left_wall or self.hit_right_wall:
			return True
		return False



######################
######################
######################
######################
######################



class physics:
#Every progressive movement is processed here.
#Block movements aren't.

	xVel, yVel = 0, 0
	xLim, yLim = 10, 10

	gravity = 0.3
	default_gravity = gravity

	def bind(self, cbox): #init
		self.cbox = cbox

	def __call__(self): #main
		self.cbox.collision.next\
		.store_move(self.xVel, self.yVel)

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


	#States

	@property
	def falling(self): return bool(self.yVel > 0)
	@property
	def rising(self): return bool(self.yVel < 0)
	@property
	def moving(self): return bool(self.xVel != 0)



######################
######################
######################
######################
######################



class controls(object):
#Awaits player key presses, performs a different action
#based on context.

	def bind(self, physics, collision, cbox):
		self.physics = physics
		self.collision = collision
		self.cbox = cbox
		#
		self._init()


	# STATES

	def _init(self): #init
		self._reset()
		self.facing_left = False

	@property
	def facing_right(self):
		return not self.facing_left
	@facing_right.setter
	def facing_right(self, arg):
		self.facing_left = not arg


	def _reset(self): #init, wall_hang
		#States
		self.idle = state_domino(True)
		self.moving = state_domino(False)
		self.diving = state_domino(False)
		self.clinging = state_domino(False)
		self.crouching = state_domino(False)
		self.crawling = state_domino(False)
		self.slide_kicking = state_domino(False)
		self.wall_hanging = state_domino(False)

		self.dominos = [self.idle, self.moving,\
			self.diving, self.clinging,\
			self.crouching, self.crawling,\
			self.slide_kicking, self.wall_hanging]
		self.wall_hanging.dominos_before(self.dominos[:-1])

		#Special
		#start at wall_hang, stop at change_sprite
		self.animate_crawl_to_hang = False



	# METHODS

	def __call__(self, key): #main
	#Key presses are made into player actions.

		#Flags
		left = key.LEFT
		right = key.RIGHT
		up = key.UP #UNUSED
		down = key.DOWN
		jump = key.Z
		action = key.X #UNUSED


		#Controls
		if self.dominos[-1].all_false(): self.idle(True)

		if not self.wall_hanging():
			if not self.slide_kicking():
				self.jump(jump)
				if not self.crouching():
					self.move(left, right)

			self.dive(down)

			self.slide_kick(down)
			self.crouch(down)
			self.crawl(left, right)

			#Wall
			self.wall_jump(jump)
		self.wall_hang(left, right, up, down, jump)
		if not self.wall_hanging(): self.cling(left, right)


	def change_sprite(self, sprite, cbox, d_move): #_.draw
	#How the state handling affects the sprite to choose.
		
		#sprite > cbox position
		sprite.x, sprite.y = cbox.x, cbox.y
		sprite.move(d_move)


		#Direction
		if self.facing_right:
			if sprite.clip.flipped:
				sprite.clip.flip()
		if self.facing_left:
			if not sprite.clip.flipped:
				sprite.clip.flip()



		# Jumping/Standing/Walking
		if self.idle() or self.moving():
			if self.collision.in_air:
				if self.physics.rising:
					sprite.clip.use(2, 0)
				if self.physics.falling:
					sprite.clip.use(4, 0)

			elif self.idle():
				sprite.clip.use(0, 0)

			elif self.moving():
				sequence = ((1,1),(0,1),(3,1),(2,1))
				sprite.animation.clips = sequence
				sprite.animation.interval = 0.1
				sprite.animation.loop = True

		#Special
		if self.clinging(): sprite.clip.use(0,2)
		if self.slide_kicking(): sprite.clip.use(0,4)

		if self.crouching():
			if self.physics.moving:
				sequence = []
				for i in range(6): sequence.append((i,3))
				sprite.animation.clips = sequence
				sprite.animation.interval = 0.05
				sprite.animation.loop = True
			else:
				sprite.clip.use(0,3)


		if self.wall_hanging():

			if self.animate_crawl_to_hang:
				sequence = []
				for i in range(1,6): sequence.append((i,2))
				sprite.animation.clips = sequence
				sprite.animation.interval = 0.1
				sprite.animation.loop = False

				#sprite > cbox position
				x = -12
				if self.facing_right: x = -x
				sprite.move((x,-1))

				if sprite.animation.has_ended:
					self.animate_crawl_to_hang = False
			else:
				sprite.clip.use(1,2)


	# ACTIONS
	
	def move(self, left, right):
		
		#Stop
		self.moving(False)

		#Start
		if left.held() or right.held():
			self.moving(True)

		#Effect
		amt = 0.15
		walkLim = 3

		if self.moving():

			if left.held():

				self.facing_left = True
				if -walkLim <= self.physics.xVel - amt:
					self.physics.move(-amt, 0)
				self.physics.right_slowdown(amt)


			if right.held():
				
				self.facing_right = True
				if self.physics.xVel + amt <= walkLim:
					self.physics.move(+amt, 0)
				self.physics.left_slowdown(amt)

		elif not self.collision.in_air:
			self.physics.x_slowdown()


	def jump(self, jump):

		#Effect
		if jump.pressed():
			if self.collision.hit_top_wall:
				self.physics.yVel = -5.5


	def dive(self, down):

		#Stop
		was_diving = self.diving.state
		self.diving(False)
		
		#Start
		if self.collision.in_air and down.pressed():
			self.diving(True)
		
		#Effect
		if self.diving() and not was_diving:
			if self.clinging: self.physics.move(y= +2)
			else: self.physics.move(y = +8)



	def slide_kick(self, down):

		#Stop
		was_slide_kicking = self.slide_kicking.state
		if self.physics.xVel == 0:
			self.slide_kicking(False)

		#Start
		if down.held() and self.physics.moving:
			if not self.collision.in_air:
				if not self.crouching():
					self.slide_kicking(True)

		#Effect (2)

			#Increase SPEED.
		if self.slide_kicking() and not was_slide_kicking:
			if self.facing_left:  self.physics.move(x= -4)
			if self.facing_right: self.physics.move(x= +4)

			#Use a DECAYED SLOWDOWN.
		if self.slide_kicking():
			if not self.collision.in_air:
				self.physics.x_slowdown(0.25)


	def crouch(self, down):

		#Stop
		was_crouching = self.crouching.state
		self.crouching(False)

		#Start
		if self.slide_kicking(): return
		if down.held() and not self.collision.in_air:
			self.crouching(True)

		#Effect
		if self.crouching() and not was_crouching:
			self.physics.xVel = 0
	
	#
	def crawl(self, left, right):

		#Effect
		if self.crouching():

			speed, limit = 1, 1

			#! Crudely COPY AND PASTED from walk.
			if left.held():	
				self.facing_left = True
				if -limit <= self.physics.xVel - speed:
					self.physics.move(-speed, 0)
				self.physics.right_slowdown(speed)

			elif right.held():
				self.facing_right = True
				if self.physics.xVel + speed <= limit:
					self.physics.move(+speed, 0)
				self.physics.left_slowdown(speed)
			#
			else:
				self.physics.x_slowdown()



	# WALL

	def cling(self, left, right):

		#Stop
		was_clinging = self.clinging.state
		self.clinging(False)
		if not self.diving():
			self.physics.gravity\
			= self.physics.default_gravity

		#Start
		if self.collision.in_air and self.collision.overlap_side_wall:
			if self.collision.hit_right_wall and self.facing_left\
			or self.collision.hit_left_wall and self.facing_right:
				self.clinging(True)

		#Effect
		if self.clinging():
			if not self.diving() and self.physics.falling:
				self.physics.gravity = 0.02
				if not was_clinging: self.physics.yVel = 0



	def wall_jump(self, jump):

		#Effect
		if self.clinging() and jump.pressed():
			if self.facing_left:
				self.physics.xVel = 4.5
				self.facing_right = True
			elif self.facing_right:
				self.physics.xVel = -4.5
				self.facing_left = True
			self.physics.yVel = -4


	def wall_hang(self, left, right, up, down, jump):
	#If the entity's top passes the wall's top.

		was_wall_hanging = self.wall_hanging.state

		#Start (2)
		def start():
			self._reset()
			self.wall_hanging(True)


		if self.collision.top_passed_top_wall\
		and self.collision.hit_side_wall:
			start()
			self.cbox.y = self.collision._top_passed_tile_y1

		if self.crouching() and self.physics.moving:

			if self.facing_left:
				if self.collision.left_passes_left_wall:
					start()
					self.animate_crawl_to_hang = True
					self.facing_right = True

					x = self.collision._left_passes_tile_x1
					y = self.collision._side_passes_tile_y1
					self.cbox.x = x
					self.cbox.y = y


			if self.facing_right:
				if self.collision.right_passes_right_wall:
					start()
					self.animate_crawl_to_hang = True
					self.facing_left = True
					
					x = self.collision._right_passes_tile_x2
					y = self.collision._side_passes_tile_y1
					self.cbox.x = x
					self.cbox.y = y


		#Effect/Stop
		if self.wall_hanging():
			self.physics.xVel, self.physics.yVel = 0, 0

			#Cancel
			if down.pressed() or jump.pressed():
				self.wall_hanging(False)

				if jump.pressed(): self.physics.move(y=-4)



class state_domino(object): #control
#When the domino falls, so do those before it.
#FALSE all the states before a TRUE domino.

	def __init__(self, truth):
		self.state = truth


	def dominos_before(self, dominos):
		self._dominos_before = dominos

		#Every domino before it is given the rest,
		#recursed until the very last domino.
		if len(dominos) > 0:
			dominos[-1].dominos_before(dominos[:-1])


	def __call__(self, truth=None):
		if truth == None: return self.state

		self.state = truth
		if truth == True:
			for state in self._dominos_before:
				state(False)



	#Utilities

	def all_false(self):
		truth = True
		for state in self._dominos_before + [self]:
			if state() == True:
				truth = False
		return truth