from code.pysfml_game import GameRectangle
from code.pysfml_game import MyTexture, MySprite

class entity(GameRectangle): #template
# * Grabs name and position.
# * Assumes a sprite exists for it. Renders and draws it.
# * Uses GameRectangle positioning.

# And, grandly:
# * Provides every single method it's hierachy references.
# * IDs every single differently named entity.

	####
	# Must NOT be totally overriden, as:
	# * It contains important init values.
	# * It contains and handles sub-class IDs.

	def __init__(self, name, tile_x, tile_y):
		self.name = name
		self.tile_x = tile_x
		self.tile_y = tile_y

		self.w, self.h = 25, 25
		self.sprite = None

		self._init_subclass_ids()

	###

	def render(self):
		d = "assets/entities/shared/%s/sheet.png"\
		% self.name
		t = MyTexture(d)
		sprite = MySprite(t)
		sprite.position = self.position
		#
		self.sprite = sprite

	def draw(self):
		if self.sprite != None: self.sprite.draw()

	###

	def react(self, Player):
		pass


	###
	# LEVEL EDITOR

	def can_save(self): #level editor
	#Prevent saving if inappropriately placed.
		return True





	#######################
	# SUB-CLASS ID'ing

	__all__ = {}
	id = 0

	def _init_subclass_ids(self): #init
		self._contain_instance()
		self._get_id()


	def _contain_instance(self): #init_subclass_ids
		name = self.__class__.__name__
		try:
			entity.__all__[name].append(self)
		except:
			entity.__all__[name] = [self]

	def _get_id(self): #init_subclass_ids
		name = self.__class__.__name__
		self.id = len(entity.__all__[name])-1