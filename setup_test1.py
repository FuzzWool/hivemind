import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1


texture = MyTexture("img/tilemaps/level.png")
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
		pass

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite.draw()

	#
	window.view = Camera
	window.display()