# Cover an object in dust.

import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

texture = MyTexture("assets/levels/shared/level1.png")
sprite = MySprite(texture)
sprite.clip.set(25, 25)
sprite.clip.use(0, 0)
sprite.position = 30,30


#

from code.pysfml_game import particle_generator
pg = particle_generator()

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pg.create(100, sprite.points)
		sprite.texture = None

	#Animation
	#
	key.reset_all()

	#Video
	window.view = Camera
	window.clear(sf.Color.WHITE)
	#
	sprite.animation.play()
	sprite.draw()
	pg.draw()
	#
	window.display()