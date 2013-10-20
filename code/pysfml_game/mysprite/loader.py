from code.pysfml_game import GameRectangle

class MySprite_Loader(GameRectangle):
# Contains a MySprite which is loaded while on Camera,
# and unloaded otherwise.

	def __init__(self):
		self.sprite = None
		
		#Load the sprite in advance to get the position.
		self.load()
		self._update_position()
		self.unload()

	#PUBLIC
	#Loading and drawing absolutely MUST be done here.

	def load(self, args=None): #override (mandatory)
		pass

	def draw(self, camera, args=None): # (mandatory)
		#Exit
		if self.sprite == None \
		and not self.in_bounds(camera):
			return

		#Events
		self._events(camera, args)

		#Draw
		if self.sprite != None:
			self.sprite.draw()

	def unload(self): #override (optional)
		self.sprite = None


	# PRIVATE
	# Update this class' positioning behind the scenes.
	# It holds on to Sprite positioning for bounds checks.

	def _events(self, camera, args=None): #draw
	#The loading event handling.
		self._update_position()

		#Unload
		if not self.in_bounds(camera):
			if self.sprite != None:
				self.unload()
		#load
		else:
			if self.sprite == None:
				self.load(args)



	x,y,w,h = 0,0,0,0
	def _update_position(self): #_events, init
		if self.sprite == None: return
		self.x, self.y, self.w, self.h \
		= self.sprite.points