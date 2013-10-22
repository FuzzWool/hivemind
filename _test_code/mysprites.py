import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MySprite, MyTexture
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

sprites = []
texture = MyTexture("assets/levels/shared/level1.png")
for x in range(10):
	sprites.append([])
	for y in range(20):
		sprite = MySprite(texture)
		sprite.clip.set(25, 25)
		sprite.clip.use(0, 0)
		sprite.position = x*25, y*25
		sprites[x].append(sprite)

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

	for x in sprites:
		for y in x:
			y.draw()

	#
	window.view = Camera
	window.display()