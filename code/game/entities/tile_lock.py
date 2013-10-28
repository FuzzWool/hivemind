from code.game.entities.entity import entity

from code.pysfml_game import MyTexture, MySprite

class tile_lock(entity):
# * WIP - Waits for a tile_key to unlock it.
# * WIP - Once so, it removes the tile it is occupying.


	def __init__(self, args):
		entity.__init__(self, args)
		#
		self.locked = True

	####

	def render(self):
		if self.locked:
			entity.render(self)

	def react(self):
		WorldMap = self.WorldMap

		key = entity.__all__["tile_key"][self.id]
		if key.collected and self.locked:
			if self.locked:
				x,y = self.tile_x, self.tile_y
				WorldMap.tiles[x][y].change("____")
				#
				self.locked = False


	####

	def can_save(self):

		#There's a KEY for every lock.
		locks = entity.__all__["tile_lock"]
		keys = entity.__all__["tile_key"]
		try: keys[self.id]
		except:
			print "! Lock has no Key with the same ID."
			
			print "Locks: ",[l.id for l in locks]
			print "Keys: ",[k.id for k in keys]
			return False

		#The lock is NOT covering a tile.
		x, y = self.tile_position
		tile = self.WorldMap.tiles[x][y]
		if tile.data == "____":
			print "! Lock placed on top of empty tile."
			return False

		return True