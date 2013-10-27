from code.pysfml_game import MyTexture, MySprite


class entity:
# * Creates orbs entities.
# * WIP - Loading/Saving

	#A cursor of the selected entity.
	def __init__(self, entities):
		self.entities = entities

		t = MyTexture\
		("assets/entities/shared/tile_key/sheet.png")
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
		name = "tile_key"
		x,y = cursor.tile_position
		self.entities.create(name, x,y)

	def _remove(self, cursor): #controls
		x,y = cursor.tile_position
		self.entities.remove(x,y)