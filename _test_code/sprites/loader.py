import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0


####
from code.pysfml_game import GameRectangle

class MySprite_Loader(GameRectangle):
# Contains a MySprite which is loaded while on Camera,
# and unloaded otherwise.

	def __init__(self):
		self.sprite = None



	#PUBLIC
	#Loading and drawing absolutely MUST be done here.

	def load(self): #override (mandatory)
		pass

	def draw(self, camera): # (mandatory)
		self._events(camera)
		if self.sprite != None:
			self.sprite.draw()

	def unload(self): #override (optional)
		self.sprite = None


	# PRIVATE
	# Update this class' positioning behind the scenes.
	# It holds on to Sprite positioning for bounds checks.

	def _events(self, camera): #draw
	#The loading event handling.
		self._update_position()

		#load
		if self.in_bounds(camera):
			if self.sprite == None:
				self.load()
				print "LOADED!"

		#Unload
		if not self.in_bounds(camera):
			if self.sprite != None:
				self.unload()
				print "Unloaded."


	x,y,w,h = 0,0,0,0
	def _update_position(self): #_events
		if self.sprite == None: return
		self.x, self.y, self.w, self.h \
		= self.sprite.points



####

class tile_sprite(MySprite_Loader):
	
	def load(self):
		texture = \
		MyTexture("assets/levels/shared/level1.png")
		sprite = MySprite(texture)
		sprite.clip.set(25, 25)
		sprite.clip.use(0, 0)
		sprite.goto = 25, 25
		self.sprite = sprite


sprite_l = tile_sprite()


#########################################################

running = True
while running:
	#Logic
	if quit(): running = False

	amt = 10
	if key.A.pressed(): Camera.x -= amt
	if key.D.pressed(): Camera.x += amt
	if key.W.pressed(): Camera.y -= amt
	if key.S.pressed(): Camera.y += amt


	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite_l.draw(Camera)

	#
	window.view = Camera
	window.display()