#Make a new ROOM class from scratch.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0,0

#########################################################


##Create STATIC MAPS.
x_tiles, y_tiles = 500,500

total_tiles = x_tiles*y_tiles
shape = sf.PrimitiveType.QUADS
#
room = sf.VertexArray(shape)

#add each tile
for x in range(x_tiles):
	for y in range(y_tiles):
		#points
		point1 = sf.Vertex()
		point2 = sf.Vertex()
		point3 = sf.Vertex()
		point4 = sf.Vertex()
		points = [point1,point2,point3,point4]

		#position
		from modules.pysfml_game.window import GRID
		x1, x2 = x*GRID, (x+1)*GRID
		y1, y2 = y*GRID, (y+1)*GRID
		#
		point1.position = x1, y1
		point2.position = x2, y1
		point3.position = x2, y2
		point4.position = x1, y2

		#texture
		point1.tex_coords = 0, 0
		point2.tex_coords = 0, GRID
		point3.tex_coords = GRID, GRID
		point4.tex_coords = GRID, 0

		#append
		for point in points:
			room.append(point)
##



texture = MyTexture("img/tilemaps/level.png")
states = sf.graphics.RenderStates()
states.texture = texture
######


running = True
while running:
	
	#LOGIC
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	amt = 5
	if key.LEFT.held(): Camera.x -= amt
	if key.RIGHT.held(): Camera.x += amt
	if key.UP.held(): Camera.y -= amt
	if key.DOWN.held(): Camera.y += amt

	#VIDEO
	window.clear(sf.Color.WHITE)
	window.view = Camera
	#
	window.draw(room, states)
	#
	window.display()