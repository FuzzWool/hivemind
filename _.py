import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

texture = MyTexture("assets/levels/shared/level1.png")
sprite = MySprite(texture)
sprite.clip.set(25, 25)
sprite.clip.use(0, 0)
sprite.position = 300,300


sprite.animation.y.end = sprite.y+0.1
sprite.animation.y.speed = -8
sprite.animation.y.vel = 1


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

	sprite.animation.play()
	sprite.draw()

	#
	window.view = Camera
	window.display()