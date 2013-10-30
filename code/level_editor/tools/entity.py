from code.pysfml_game import MyTexture, MySprite

# ! Created for each individual entity, name just differs.
# This is just for consistency in the toolbox icons.

class entity(object):
# * Creates and removes entities.

	name = "tile_key"

	def __init__(self, entities, name):
		self.entities = entities
		self.name = name
		self._render_cursor()

	def controls(self, mouse, cursor):
		self.cursor.center = cursor.center
		if mouse.left.held(): self._create(cursor)
		if mouse.right.held(): self._remove(cursor)

	def draw(self):
		if self.cursor: self.cursor.draw()
	#


	def _create(self, cursor): #controls
		name = self.name
		x,y = cursor.tile_position
		self.entities.create(name, x,y)

	def _remove(self, cursor): #controls
		x,y = cursor.tile_position
		self.entities.remove(x,y)

	#

	_name = "tile_key"
	@property
	def name(self): return self._name
	@name.setter
	def name(self, name):
		self._name = name
		self._render_cursor()


	def _render_cursor(self): #init, name
		name = self.name
		d = "assets/entities/shared/%s/sheet.png" % name
		t = MyTexture(d)
		self.cursor = MySprite(t)
