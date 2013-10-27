import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

texture = MyTexture("assets/levels/shared/level1.png")
sprite = MySprite(texture)
# sprite.clip.set(25, 25)
# sprite.clip.use(0, 0)
sprite.position = 100,100

#####

from code.pysfml_game import oscillate

animation_y = oscillate()
animation_y.speed = +3
animation_y.vel = -0.1
animation_y.end = sprite.y

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

	sprite.y += animation_y.play(sprite.y)
	sprite.draw()
	#
	window.view = Camera
	window.display()