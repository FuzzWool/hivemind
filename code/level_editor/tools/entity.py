from code.pysfml_game import MyTexture, MySprite

# ! Created for each individual entity, name just differs.
# This is just for consistency in the toolbox icons.

class entity:
# * Creates and removes entities.

	name = "tile_key"

	#A cursor of the selected entity.
	def __init__(self, entities, name):
		self.entities = entities
		self.name = name

		d = "assets/entities/shared/%s/sheet.png" % name
		t = MyTexture(d)
		self.cursor = MySprite(t)

	def controls(self, mouse, cursor):
	#Create entities upon clicking.
		self.cursor.center = cursor.center

		if mouse.left.held(): self._create(cursor)
		if mouse.right.held(): self._remove(cursor)

	def draw(self):
		if self.cursor: self.cursor.draw()
	#


	def _create(self, cursor): #controls
	#Create an entity in the selected tile.
		name = self.name
		x,y = cursor.tile_position
		self.entities.create(name, x,y)

	def _remove(self, cursor): #controls
		x,y = cursor.tile_position
		self.entities.remove(x,y)