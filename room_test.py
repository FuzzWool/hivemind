#Make a new ROOM class from scratch.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0,0


#####
from modules.pysfml_game import\
 RENDER_WIDTH, RENDER_HEIGHT
from modules.pysfml_game import GRID

class Room(object):

	# SPRITE HANDLING

	def __init__(self, x=0, y=0):
		self.texture = MyTexture("img/tilemaps/level.png")
		self.x, self.y = x, y
		self.tiles = self.load(self.x, self.y)

	def load(self, room_x=0, room_y=0):
		#LOAD and POSITION the tiles.
		#Consider the ROOM OFFSET, too!
		tiles = []
		w, h = RENDER_WIDTH/GRID, RENDER_HEIGHT/GRID
		room_x *= RENDER_WIDTH/GRID
		room_y *= RENDER_HEIGHT/GRID

		for x in range(w):
			tiles.append([])
			for y in range(h):
				tile = self.Tile()
				tile.load(self.texture)
				tile.x, tile.y = room_x+x, room_y+y
				tiles[-1].append(tile)
		return tiles

	def draw(self):
		for x in self.tiles:
			for y in x:
				y.draw()



	class Tile(object):

		def __init__(self):
			self.sprite = None

		# SPRITE HANDLING

		def load(self, texture):
			self.sprite = MySprite(texture)
			self.sprite.clip.set(GRID,GRID)

		def draw(self):
			self.sprite.draw()

		# POSITION

		@property
		def x(self): return self.sprite.x/GRID
		@x.setter
		def x(self, x): self.sprite.x = x*GRID
		#
		@property
		def y(self): return self.sprite.y/GRID
		@y.setter
		def y(self, y): self.sprite.y = y*GRID


####




room = Room(0,0)

#########################################################

running = True
while running:
	
	#LOGIC
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#VIDEO
	window.clear(sf.Color.WHITE)
	window.view = Camera
	
	room.draw()

	window.display()