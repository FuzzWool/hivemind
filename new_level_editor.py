from code.pysfml_game import sf
from code.pysfml_game import quit
from code.pysfml_game import window
from code.pysfml_game import key
from code.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

from code.game import WorldMap
worldmap = WorldMap(4,4)


###########
from code.pysfml_game import MyTexture, MySprite

class toolbox:
	
	def __init__(self):
	#Create a cursor.
		cursor_tex \
		= MyTexture("assets/level_editor/cursor.png")
		self.cursor = MySprite(cursor_tex)

	def draw(self, mouse):
	#Position and draw the cursor.
		self.cursor.tile_position = mouse.tile_position
		self.cursor.draw()



#########################################################
from code.pysfml_game import MyMouse

mouse = MyMouse()
TB = toolbox() ###


running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#Video
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()

	TB.draw(mouse) ###

	#
	window.display()