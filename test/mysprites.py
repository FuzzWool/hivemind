import modules as mo
rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)

tex = mo.sf.Texture.load_from_file("img/test/test.png")
sprites = []
def make_sprite():
	i = len(sprites)
	sprite = mo.MySprite(tex)
	sprite.clip.set(25, 25)
	sprite.clip.use(i, 0)
	sprite.position = 100 + (i * 50), 100
	sprites.append(sprite)

for i in range(5):
	make_sprite()

#########################################################
running = True
while running:
	
	#Logic
	if mo.quit(): running = False
	if rtrn.pressed():
		pass

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#
	for s in sprites:
		s.draw()
	#
	mo.window.display()