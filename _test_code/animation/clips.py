import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

sprites = []
texture = MyTexture("img/tilemaps/level.png")
for x in range(1):
	sprites.append([])
	for y in range(1):
		sprite = MySprite(texture)
		sprite.clip.set(25, 25)
		sprite.clip.use(0, 0)
		sprite.goto = x*25, y*25
		sprites[x].append(sprite)

sprites[0][0].goto = 100, 100

#Make a light sequence.
clip_sequence = ((0,0),(0,1),(0,2))
sprites[0][0].animation.clips = clip_sequence

#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():

		#Interrupt the sequence.
		sprites[0][0].clip.use(1,0)

	#Animation
	#
	sprites[0][0].animation.play()

	#Video
	window.clear(sf.Color.WHITE)
	#

	for x in sprites:
		for y in x:
			y.draw()

	#
	window.view = Camera
	window.display()