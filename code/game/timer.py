import sfml as sf
from code.pysfml_game import window
from code.pysfml_game import MyTexture, MySprite
from code.pysfml_game import GameRectangle

class Timer(GameRectangle):
	
	def __init__(self):
		self._init_graphics()
		self.stop()
		self.position = 5,5


	def draw(self):
		self._update_state()

		window.draw(self.box)
		for sprite in self.sprites:
			sprite.draw()


	# States

	def stop(self):
		self._falsify()
		self.stopped = True
		self.box.fill_color = sf.Color(200,200,200,255)

	def start(self):
		if self.stopped: self.clock.restart()

		self._falsify()
		self.started = True
		self.box.fill_color = sf.Color(255,255,255,255)


	###

	stopped = False
	started = False

	clock = sf.Clock()

	def _falsify(self): #stop, start
		self.stopped = False
		self.started = False


	def _update_state(self): #draw
		if self.started: self._update_start()

	def _update_start(self): #update_start
		#update the counter sprites.
		secs = int(self.clock.elapsed_time.seconds)

		if secs > 5999: self.stop()

		#indiv values
		secs1 = secs
		secs2 = secs
		while secs2 > 60: secs2 -= 60
		secs2 = secs2/10
		mins1 = secs/60
		mins2 = secs/600

		while secs1 > 9: secs1 -= 10
		while secs2 > 60: secs2 -= 60
		while secs2 > 5: secs2 -= 10
		while mins1 > 9: mins1 -= 10
		while mins2 > 9: mins2 -= 10

		if secs1 < 0: secs1 = 0
		if secs2 < 0: secs2 = 0
		if mins1 < 0: mins1 = 0
		if mins2 < 0: mins2 = 0


		#update sprites
		self.count_sprites[-1].clip.use(secs1, 0)
		self.count_sprites[-2].clip.use(secs2, 0)
		self.count_sprites[-3].clip.use(mins1, 0)
		self.count_sprites[-4].clip.use(mins2, 0)

		if mins2 == 0:
			self.count_sprites[-4].clip.use(12,0)

	########

	# Graphics - init, draw

	def _init_graphics(self): #init
		self._init_sprites()
		self._load_sprites()
		self._label_sprites()
		self._create_box()


	def _init_sprites(self): #init_graphics
		self.sprites = []

	def _load_sprites(self): #init_graphics
		d = "assets/timer/sheet.png"
		t = MyTexture(d)

		for i in range(6):
			s = MySprite(t)
			s.clip(13,20)
			s.clip.use(0,0)
			s.position = i*13,0

			self.sprites.append(s)

	def _label_sprites(self): #init_graphics
		self.clock_sprite = self.sprites[0]
		self.colon_sprite = self.sprites[3]
		self.count_sprites = \
		self.sprites[1:3]+self.sprites[4:]

		self.clock_sprite.clip.use(11,0)
		self.colon_sprite.clip.use(10,0)

	#

	def _create_box(self): #init_graphics
		box = sf.RectangleShape()
		box.outline_color = sf.Color(0,0,0,255)
		box.outline_thickness = 1

		#grab points
		x, y = box.position
		w = self.sprites[-1].x2 - self.sprites[0].x1
		h = self.sprites[0].h

		box.size = w+1,h+1
		self.box = box

	####

	#Position - graphics

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