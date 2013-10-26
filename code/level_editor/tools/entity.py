from code.pysfml_game import MyTexture, MySprite


class entity:
# * WIP - positions entities within the WorldMap.

	#A cursor of the selected entity.
	def __init__(self):
		t = MyTexture\
		("assets/entities/shared/orb/sheet.png")
		self.cursor = MySprite(t)

	def controls(self, cursor):
		self.cursor.center = cursor.center

	def draw(self):
		if self.cursor: self.cursor.draw()
	#