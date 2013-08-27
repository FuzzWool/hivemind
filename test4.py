#Make a blank MySprite which can have it's color set.
#(Solid then transparent)

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0


#
# texture = sf.Texture.from_file("img/tilemaps/level.png")
texture = sf.Texture.create(25,25)
#
sprite = MySprite(texture)
sprite.clip.set(25, 25)
sprite.clip.use(0, 0)
sprite.goto = 25, 25

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		print sprite.color

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite.draw()

	#
	window.view = Camera
	window.display()