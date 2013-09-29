#Make a new ROOM class from scratch.

import modules.pysfml_game.key as key
from modules.pysfml_game import quit, window, sf
from modules.pysfml_game import MySprite, MyTexture
from modules.pysfml_game import MyCamera

Camera = MyCamera()
Camera.zoom = 1
Camera.x, Camera.y = 0,0

#########################################################

box = sf.VertexArray(sf.PrimitiveType.QUADS,8)
box[0].position = 0,0
box[1].position = 100,0
box[2].position = 100,100
box[3].position = 0,100

box[4].position = 100,100
box[5].position = 200,100
box[6].position = 200,200
box[7].position = 100,200


amt = 50
box[0].tex_coords = 0,0
box[1].tex_coords = amt,0
box[2].tex_coords = amt,amt
box[3].tex_coords = 0,amt

box[4].tex_coords = amt,amt
box[5].tex_coords = amt*2,amt
box[6].tex_coords = amt*2,amt*2
box[7].tex_coords = amt,amt*2



texture = MyTexture("img/tilemaps/level.png")
states = sf.graphics.RenderStates()
states.texture = texture
######


running = True
while running:
	
	#LOGIC
	if quit(): running = False
	if key.RETURN.pressed():
		pass

	amt = 5
	if key.LEFT.held(): Camera.x -= amt
	if key.RIGHT.held(): Camera.x += amt
	if key.UP.held(): Camera.y -= amt
	if key.DOWN.held(): Camera.y += amt

	#VIDEO
	window.clear(sf.Color.WHITE)
	window.view = Camera
	#
	window.draw(box, states)
	#
	window.display()


# // create an array of 3 vertices that define a box primitive
# sf::VertexArray box(sf::boxs, 3);

# // define the position of the box's points
# box[0].position = sf::Vector2f(10, 10);
# box[1].position = sf::Vector2f(100, 10);
# box[2].position = sf::Vector2f(100, 100);

# // define the color of the box's points
# box[0].color = sf::Color::Red;
# box[1].color = sf::Color::Blue;
# box[2].color = sf::Color::Green;

# // no texture coordinates here, we'll see that later