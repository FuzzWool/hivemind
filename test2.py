#Testing slope collision.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

###########

#Box
box_tex = MyTexture("img/characters/nobody/cbox.png")
box = MySprite(box_tex)
box.goto = 25, 25

#TRIANGLE
triangle_tex = MyTexture("img/triangle3.png")
triangle = MySprite(triangle_tex)
triangle.goto = 200, 150

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
box.axis_collision.init_angles(triangle, points)
#####

#########################################################
running = True
while running:
	#Logic
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	amt = 5
	if key.A.held(): box.move(-amt, 0)
	if key.D.held(): box.move(+amt, 0)
	if key.W.held(): box.move(0, -amt)
	if key.S.held(): box.move(0, +amt)

	box.axis_collision.observe_angles(triangle)
	box.axis_collision.pushback(triangle)

	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#
	triangle.draw()
	box.draw()
	box.axis_collision.draw(triangle)
	#
	window.view = Camera
	window.display()