#Work out how much area is covered between two MySprites
#for...
# X
# Y

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

texture = MyTexture("img/tilemaps/level2.png")

sprite1 = MySprite(texture)
sprite1.clip.set(25,25)
sprite1.clip.use(1, 0)
sprite1.goto = 100,100

sprite2 = MySprite(texture)
sprite2.clip.set(50,50)
sprite2.goto = 200, 200
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():

		#!!! Has to keep negative values.
		print sprite1.overlap.y(sprite2)

	amt = 2
	if key.W.held(): sprite1.move(y= -amt)
	if key.S.held(): sprite1.move(y= +amt)
	if key.A.held(): sprite1.move(x= -amt)
	if key.D.held(): sprite1.move(x= +amt)

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite2.draw()
	sprite1.draw()
	#
	window.view = Camera
	window.display()