#Testing side collisions for slopes

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0, 0

#Box
box_tex = MyTexture("img/characters/nobody/cbox.png")
box = MySprite(box_tex)
box.goto = 25, 25

#TRIANGLE
triangle_tex = MyTexture("img/triangle1.png")
triangle = MySprite(triangle_tex)
triangle.goto = 200, 200
#####

hypo = "rd"

t = triangle
if hypo == "rd":
	\
					  c = (t.x2, t.y1)
	a = (t.x1, t.y2)

if hypo == "ru":
	\
	c = (t.x1, t.y1);\
					  a = (t.x2, t.y2)
	triangle.clip.flip_vertical()

if hypo == "ld":
	\
	a = (t.x1, t.y1);\
					 c = (t.x2, t.y2)
	triangle.clip.flip_horizontal()

if hypo == "lu":
	\
					 c = (t.x2, t.y1)
	a = (t.x1, t.y2)
	triangle.clip.flip_vertical()
	triangle.clip.flip_horizontal()

triangle.slope_collision.a = a
triangle.slope_collision.b = c
triangle.slope_collision.anchor = hypo
print triangle.slope_collision.anchor
#########################################################
running = True
while running:
	#Logic
	if quit(): running = False

	amt = 5
	if key.A.held(): box.collision.try_move(x= -amt)
	if key.D.held(): box.collision.try_move(x= +amt)
	if key.W.held(): box.collision.try_move(y= -amt)
	if key.S.held(): box.collision.try_move(y= +amt)


	#State checks - these should come before the pushback
	if box.slope_collision.bottom_to_top(triangle):
		triangle.color = sf.Color(255,255,255,100)
	else:
		triangle.color = sf.Color(255,255,255,255)

	box.slope_collision.pushback(triangle)
	box.collision.confirm_move()

	#
	#Animation
	#

	#Video
	window.clear(sf.Color.WHITE)
	#
	triangle.draw()

	box.draw()
	triangle.slope_collision.draw()

	#
	window.view = Camera
	window.display()