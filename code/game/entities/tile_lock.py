from code.game.entities.entity import entity

from code.pysfml_game import MyTexture, MySprite

class tile_lock(entity):
# * WIP - Waits for a tile_key to unlock it.
# * WIP - Once so, it removes the tile it is occupying.

	locked = True

	def worldmap_react(self, worldmap):
		
		if self.locked:
			x,y = self.tile_x, self.tile_y
			worldmap.tiles[x][y].change("____")
			#
			self.locked = False