#Testing MySprite.overlap (x/y)

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

#Box
box_tex = MyTexture("img/characters/nut/cbox.png")
tile_tex = MyTexture("img/tilemaps/_collision.png")
box1 = MySprite(box_tex); box1.goto = 25, 25
box2 = MySprite(tile_tex); box2.goto = 50, 50
box2.clip.set(25,25)

#########################################################
running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		print box1.overlap.y(box2)



	amt = 2
	if key.A.held(): box1.collision.next.store_move(x= -amt)
	if key.D.held(): box1.collision.next.store_move(x= +amt)
	if key.W.held(): box1.collision.next.store_move(y= -amt)
	if key.S.held(): box1.collision.next.store_move(y= +amt)

	box1.collision.pushback(box2)
	box1.collision.next.confirm_move()


	#Video
	window.clear(sf.Color.WHITE)
	#
	box2.draw()
	box1.draw()
	#
	window.view = Camera
	window.display()