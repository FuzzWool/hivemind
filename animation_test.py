#MySprite.Animation tests.


import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

texture = MyTexture("assets/characters/nut/sheet.png")
sprite = MySprite(texture)
sprite.clip.set(40,40)
sprite.clip.use(0, 0)
sprite.goto = 25, 25

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		sprite.animation.loop = not sprite.animation.loop
		print sprite.animation.loop

	key.reset_all()

	#Animation
	#
	sequence = ((1,1),(0,1),(3,1),(2,1))
	sprite.animation.clips = sequence
	sprite.animation.interval = 0.1
	sprite.animation.play()

	#Video
	window.clear(sf.Color.WHITE)
	#

	sprite.draw()

	#
	window.view = Camera
	window.display()