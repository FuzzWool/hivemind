#Testing making INDEPENDANT SLOPE COLLISIONS.

#May test:
# Collisions using RECTS.
# Collisions using MYSPRITES.


import code.pysfml_game.key as key
from code.pysfml_game import quit, window, sf
from code.pysfml_game import MyCamera

from code.pysfml_game import MyTexture, MySprite


###

from code.pysfml_game import GameRectangle

from code.pysfml_game.mysprite.collision import next
from code.pysfml_game.mysprite.collision import overlap
from code.pysfml_game.mysprite.collision import collision
#
from code.pysfml_game.mysprite.collision \
import slope_collision

class TestBox(GameRectangle):
#Testing the INDEPENDANCE of collisions.

	def __init__(self, x, y, w, h):
		self.x, self.y, self.w, self.h = x, y, w, h
		self.color = sf.Color(100,100,100)
		
		self.next = next(self)
		self.collision = collision(self)
		self.slope_collision = slope_collision(self)


	# Movements need to be processed through NEXT.


	#debug
	def draw(self):
		pos = self.x, self.y
		size = self.w, self.h
		rectangle = sf.RectangleShape(size)
		rectangle.position = pos
		rectangle.fill_color = self.color
		window.draw(rectangle)



###


box1 = TestBox(0,0,100,100); box1.color = sf.Color.RED
box2 = TestBox(200,200,50,50); box2.color = sf.Color.BLUE

# texture = MyTexture("assets/levels/shared/level1.png")

# box1 = MySprite(texture)
# box1.clip.set(25,25)
# box1.position = 0,0

# box2 = MySprite(texture)
# box2.clip.set(25,25)
# box2.position = 100,100

#

c = box2.slope_collision
c.a = (box2.x2,box2.y1+10)
c.b = (box2.x1,box2.y2)
c.anchor = "rd"


Camera = MyCamera()
Camera.zoom = 2
Camera.x, Camera.y = 0,0

#########################################################

running = True
while running:
	
	#LOGIC
	if quit(): running = False
	if key.RETURN.pressed():
		print box1.position

	amt = 2
	if key.LEFT.held(): box1.collision.next.store_move(x=-amt)
	if key.RIGHT.held(): box1.collision.next.store_move(x=+amt)
	if key.UP.held(): box1.collision.next.store_move(y=-amt)
	if key.DOWN.held(): box1.collision.next.store_move(y=+amt)


	box1.slope_collision.pushback(box2)
	box1.collision.next.confirm_move()


	#VIDEO
	window.clear(sf.Color.WHITE)
	window.view = Camera

	#
	box2.draw()
	box1.draw()
	box2.slope_collision.draw()
	#


	window.display()