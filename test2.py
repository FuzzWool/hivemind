#Testing new collision predictions.
#The moving sprite1 will NEVER overlap the opposing sprite1.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

texture = MyTexture("img/tilemaps/level.png")
sprite1 = MySprite(texture)
sprite1.clip.set(25, 25)
sprite1.clip.use(0, 0)
sprite1.goto = 25, 25

sprite2 = MySprite(texture)
sprite2.clip.set(50, 25)
sprite2.clip.use(0,1)
sprite2.goto = 100, 100
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	amt = 5
	if key.W.held(): sprite1.collision.try_move(y= -amt)
	if key.S.held(): sprite1.collision.try_move(y= +amt)
	if key.A.held(): sprite1.collision.try_move(x= -amt)
	if key.D.held(): sprite1.collision.try_move(x= +amt)

	#WIP
	sprite1.collision.pushback(sprite2)
	sprite1.collision.confirm_move()
	#

	#Video
	window.clear(sf.Color.WHITE)
	#
	sprite2.draw()
	sprite1.draw()


	window.view = Camera
	window.display()