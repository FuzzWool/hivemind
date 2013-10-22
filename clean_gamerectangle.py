import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

texture1 = MyTexture("assets/characters/nobody/cbox.png")
texture2 = MyTexture("assets/characters/nobody2/cbox.png")

sprite1 = MySprite(texture1)
sprite2 = MySprite(texture2)

sprite1.position = 100,100
sprite2.position = 200,200

########################################################
# GAMERECTANGLE tests.

# ! KEEP IN BOUNDS
# ! keep_in_bounds
# ! keep_in_tile_bounds
# ! keep_in_room_bounds


# IN BOUNDS
# ! in_bounds
# ! in_tile_bounds
# ! in_room_bounds


#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite1.draw()
	sprite2.draw()

	#
	window.view = Camera
	window.display()