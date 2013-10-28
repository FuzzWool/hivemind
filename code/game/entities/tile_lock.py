from code.game.entities.entity import entity

from code.pysfml_game import MyTexture, MySprite

class tile_lock(entity):
# * WIP - Waits for a tile_key to unlock it.
# * WIP - Once so, it removes the tile it is occupying.

	locked = True

	# def react(self):
	# 	WorldMap = self.WorldMap

	# 	if self.locked:
	# 		x,y = self.tile_x, self.tile_y
	# 		WorldMap.tiles[x][y].change("____")
	# 		#
	# 		self.locked = False


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

		#The lock is COVERING a TILE.
		pass

		return True