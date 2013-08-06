from modules.pysfml_game import sf
from modules.pysfml_game import quit
from modules.pysfml_game import window
from modules.pysfml_game import key
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

from modules.game import Player
Nut = Player("nut")


#TRIANGLE
from modules.pysfml_game import MyTexture, MySprite
from modules.pysfml_game import GRID

triangle_tex = MyTexture("img/triangle3.png")
triangle = MySprite(triangle_tex)
triangle.x1 = GRID*10
triangle.y2 = GRID*9

hypo = "lu"

t = triangle
if hypo == "rd":
	\
					  a = (t.x2, t.y1)
	c = (t.x1, t.y2); b = (t.x2, t.y2);

if hypo == "ld":
	a = (t.x1, t.y1)
	b = (t.x1, t.y2); c = (t.x2, t.y2)
	triangle.clip.flip_horizontal()

if hypo == "ru":
	c = (t.x1, t.y1); b = (t.x2, t.y1);\
					  a = (t.x2, t.y2)
	triangle.clip.flip_vertical()

if hypo == "lu":
	b = (t.x1, t.y1); c = (t.x2, t.y1)
	a = (t.x1, t.y2)
	triangle.clip.flip_vertical()
	triangle.clip.flip_horizontal()

points = a, b, c
Nut.cbox.axis_collision.init_angles(triangle, points)
#####

from modules.game import WorldMap
worldmap = WorldMap()
#########################################################

running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	#WIP###
	Nut.handle_controls(key)
	Nut.handle_physics()
	Nut.collide_with_WorldMap(worldmap)

	Nut.cbox.axis_collision.observe_angles(triangle)
	Nut.cbox.axis_collision.pushback(triangle)
	###

	#Animation
	Nut.play()

	#Video
	# Camera.center = Nut.cbox.center
	worldmap.load_around(Camera.room_points, Camera.tile_points)
	
	window.view = Camera
	window.clear(sf.Color(255, 200, 200))
	#
	worldmap.draw()
	triangle.draw()
	Nut.draw()
	#
	window.display()