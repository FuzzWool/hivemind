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
sprite2.position = 300,300

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass
		# print sprite1.in_points(sprite2)

	#Animation
	#

	key.reset_all()

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite1.draw()
	sprite2.draw()

	#
	window.view = Camera
	window.display()