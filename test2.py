#TEST overlapping with slopes.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0, 0

#Box
box_tex = MyTexture("img/characters/nut/cbox.png")
box = MySprite(box_tex)
box.goto = 25, 100

#TRIANGLE
triangle_tex = MyTexture("img/tilemaps/_collision.png")
triangle = MySprite(triangle_tex)
triangle.clip.set(25,25)
triangle.clip.use(1,0)
triangle.goto = 100,200
#####

hypo = "rd"

t = triangle
if hypo == "rd":
	\
					  c = (t.x2, t.y1)
	a = (t.x1, t.y2-10)

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
	if key.RETURN.pressed():
		print box.slope_collision.y_overlap_amt(triangle)
		print "####"
		t_sc = triangle.slope_collision
		# print t_sc.left_point[0], t_sc.right_point[0]
		# print t_sc.x1, t_sc.x2
		print t_sc.up_point[1], t_sc.down_point[1]
		print t_sc.y1, t_sc.y2		

	amt = 2
	if key.LEFT.held(): box.collision.next.store_move(x= -amt)
	if key.RIGHT.held(): box.collision.next.store_move(x= +amt)
	if key.UP.held(): box.collision.next.store_move(y= -amt)
	if key.DOWN.held(): box.collision.next.store_move(y= +amt)

	box.slope_collision.pushback(triangle)
	box.collision.next.confirm_move()

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