import sfml as sf
from code.pysfml_game import MyTexture, MySprite

from code.pysfml_game import RENDER_HEIGHT, RENDER_WIDTH
from code.pysfml_game import GRID

class camera:
#WIP - Created for each room.
#Rendered ON-THE-FLY.
	

	#_LOAD
	def __init__(self, worldmap):
		self._create_locks(worldmap)

		self.worldmap = worldmap #draw

	def _create_locks(self, worldmap): #init

		self.all_locks = []
		for rooms_column in worldmap.rooms:
			self.all_locks.append([])

			for room in rooms_column:
				lock = locks(room)
				self.all_locks[-1].append(lock)
	#


	#DRAW
	def draw(self, camera):

		#Draw within camera range
		x1, y1, x2, y2 = camera.room_points
		x1, y1 = self.worldmap\
		.keep_in_room_points((x1,y1))
		x2, y2 = self.worldmap\
		.keep_in_room_points((x2,y2))

		for column in self.all_locks[x1:x2]:
			for locks in column[y1:y2]:
				locks.draw()


	#CONTROLS
	def controls(self, worldmap, mouse, cursor):
	#Press the locks in order to toggle them. 
		
		#find which lock to select
		x,y = cursor.room_position

		if 0 <= x < worldmap.room_h\
		and 0 <= y < worldmap.room_w:
			
			self.all_locks[x][y].controls\
			(mouse, cursor)



#
class locks:
#Sets camera locks for each side of a single room.

	def __init__(self, room):

		#sides
		self.left = _side("left", room)
		self.right = _side("right", room)
		self.up = _side("up", room)
		self.down = _side("down", room)
		#
		self.sides \
		= [self.left, self.right, self.up, self.down]


		#lock
		self.lock = lock(room.room_x,room.room_y)

		#set the lock's state
		any_enabled = False
		for side in self.sides:
			if side.enabled: any_enabled = True
		if any_enabled:
			self.lock.enable()



	def draw(self):
		for side in self.sides:
			side.draw()

		self.lock.draw()


	#

	def controls(self, mouse, cursor):

		pressed = mouse.left.pressed()

		#Toggle a SIDE.
		#Enable the lock if any are enabled.
		#Disable the lock if all are disabled.
		any_enabled = False

		for side in self.sides:
			if pressed:
				if cursor.in_points(side.sprite):
					side.toggle()

			if side.enabled:
				any_enabled = True
		
		if pressed:
			if any_enabled:
				self.lock.enable()
			else:
				self.lock.disable()


		#Toggle the LOCK.
		#Enables all sides if enabled.
		#Disables all sides if disabled.
		if pressed:

			if self.lock.sprite != None:
				if self.lock.sprite.in_points(cursor):
					self.lock.toggle()

					for side in self.sides:
						if self.lock.enabled:
							side.enable()
						else:
							side.disable()


from code.pysfml_game import MySprite_Loader
##
class _side(object):
#A conditions and configurations for loading the
#side sprites.

	def __init__ (self, pos, room):
		self._init_sprite(pos, room.room_x, room.room_y)
		self.pos = pos
		self.room = room
		# MySprite_Loader.__init__(self)
		self.sprite = None
		self.load()
		#
		self._init_toggle(pos, room)


	#TOGGLE
	disable_color = sf.Color(0,0,0,100)
	enable_color = sf.Color(255,255,255,255)

	def _init_toggle(self, pos, room): #init
		self.pos = pos #enabled
		self.room = room #enabled

		#
		lock = self.enabled
		#Use it.
		if lock == True: self.enable()
		if lock == False: self.disable()


	#mutated ugliness

	@property
	def enabled(self):
		pos = self.pos
		locks = self.room.camera_locks
		#
		if pos == "left": lock = locks.left
		if pos == "right": lock = locks.right
		if pos == "up": lock = locks.up
		if pos == "down": lock = locks.down
		#
		return lock
	@enabled.setter
	def enabled(self, truth):
		pos = self.pos
		locks = self.room.camera_locks
		#
		if pos == "left": locks.left = truth
		if pos == "right": locks.right = truth
		if pos == "up": locks.up = truth
		if pos == "down": locks.down = truth

	#

	def toggle(self):
		if self.enabled: self.disable()
		else: self.enable()

	def disable(self):
		self.enabled = False
		if self.sprite != None:
			self.sprite.color = self.disable_color
	def enable(self):
		self.enabled = True
		if self.sprite != None:
			self.sprite.color = self.enable_color


	#SPRITE

	x_texture = MyTexture\
	("assets/level_editor/camera/x_side.png")
	y_texture = MyTexture\
	("assets/level_editor/camera/y_side.png")

	def _init_sprite(self, pos, room_x, room_y): #init
		self.pos = pos
		self.room_x, self.room_y = room_x, room_y


	def load(self, args=None): #parent
		pos = self.pos
		room_x, room_y = self.room_x, self.room_y

		if pos in ("left","right"):
			self.sprite = MySprite(self.x_texture)

			if pos == "left":
				pass

			if pos == "right":
				self.sprite.clip.flip_horizontal()
				self.sprite.x = RENDER_WIDTH - GRID


		if pos in ("up","down"):
			self.sprite = MySprite(self.y_texture)

			if pos == "up":
				pass

			if pos == "down":
				self.sprite.clip.flip_vertical()
				self.sprite.y = RENDER_HEIGHT - GRID

		self.sprite.x += room_x*RENDER_WIDTH
		self.sprite.y += room_y*RENDER_HEIGHT

		#Render the sprite
		self.toggle(); self.toggle()

	def draw(self, args=None):
		self.sprite.draw()


from code.pysfml_game import MySprite_Loader
##
class lock():
	
	def __init__(self, room_x, room_y):
		self._init_position(room_x, room_y)
		self._init_toggle()
		# MySprite_Loader.__init__(self)
		self.load()


	#PUBLIC

	def _init_toggle(self):
		self.enabled = False
		self.disable()

	def toggle(self):
		if self.enabled: self.disable()
		else: self.enable()

	def disable(self):
		self.enabled = False
		if self.sprite != None:
			self.sprite.clip.use(1,0)
	def enable(self):
		self.enabled = True
		if self.sprite != None:
			self.sprite.clip.use(0,0)

	#

	texture = MyTexture\
	("assets/level_editor/camera/lock.png")


	def _init_position(self, room_x, room_y):
		self.sprite = None
		self.room_x, self.room_y = room_x, room_y


	def load(self, args=None):
		s = MySprite(self.texture)
		s.clip.set(100,120)
		s.center = RENDER_WIDTH/2, RENDER_HEIGHT/2
		s.x += self.room_x*RENDER_WIDTH
		s.y += self.room_y*RENDER_HEIGHT

		self.sprite = s

		self.toggle(); self.toggle() #render the sprite

	def draw(self, args=None):
		self.sprite.draw()