from code.pysfml_game import quit, window, key, sf
#########################################################
from code.pysfml_game import MyCamera
Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0


#############################
#create a timer
from code.pysfml_game import MyTexture, MySprite
from code.pysfml_game import GameRectangle

class Timer(GameRectangle):
	
	def __init__(self):
		self._init_graphics()
		self.position = 5,5


	def draw(self):
		window.draw(self.box)
		for sprite in self.sprites:
			sprite.draw()



	########

	# Graphics

	def _init_graphics(self):
		self._init_sprites()
		self._load_sprites()
		self._label_sprites()
		self._create_box()


	def _init_sprites(self):
		self.sprites = []

	def _load_sprites(self):
		d = "assets/timer/sheet.png"
		t = MyTexture(d)

		for i in range(6):
			s = MySprite(t)
			s.clip(13,20)
			s.clip.use(0,0)
			s.position = i*13,0

			self.sprites.append(s)

	def _label_sprites(self):
		self.clock_sprite = self.sprites[0]
		self.colon_sprite = self.sprites[3]
		self.count_sprites = \
		self.sprites[1:3]+self.sprites[4:]

		self.clock_sprite.clip.use(11,0)
		self.colon_sprite.clip.use(10,0)

	#

	def _create_box(self):
		box = sf.RectangleShape()
		box.outline_color = sf.Color(0,0,0,255)
		box.outline_thickness = 1

		#grab points
		x, y = box.position
		w = self.sprites[-1].x2 - self.sprites[0].x1
		h = self.sprites[0].h

		# box.fill_color = sf.Color(200,200,200,255)

		box.size = w+1,h+1
		self.box = box

	####

	#Position

	@property
	def x(self): return self.box.position[0]
	@x.setter
	def x(self, x): #move the box and the sprites
		move_amt = x - self.box.position[0]
		for sprite in self.sprites:
			sprite.x += move_amt
		self.box.position = x, self.box.position[1]

	@property
	def y(self): return self.box.position[1]
	@y.setter
	def y(self, y): #move the box and the sprites
		move_amt = y - self.box.position[1]
		for sprite in self.sprites:
			sprite.y += move_amt
		self.box.position = self.box.position[0], y


	@property
	def w(self): return self.box.size[0]
	@property
	def h(self): return self.box.size[1]


##############################

timer = Timer()


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed(): pass
	key.reset_all()


	#Video
	window.view = Camera
	window.clear(sf.Color(255,200,200))
	
	timer.draw()
	
	window.display()
