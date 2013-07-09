import sfml as sf

SCALE = 2
GRID = 25

SCREEN_WIDTH = 400 * SCALE
SCREEN_HEIGHT = 300 * SCALE
RENDER_WIDTH = SCREEN_WIDTH / SCALE
RENDER_HEIGHT = SCREEN_HEIGHT / SCALE

ROOM_SIZE = [RENDER_WIDTH, RENDER_HEIGHT]
ROOM_WIDTH = ROOM_SIZE[0]
ROOM_HEIGHT = ROOM_SIZE[1]

#

window = \
	sf.RenderWindow(\
		sf.VideoMode\
		 (SCREEN_WIDTH, SCREEN_HEIGHT), "Hivemind")
window.framerate_limit = 60
window.vertical_sync_enabled = True

view = sf.View.from_rect(\
	sf.FloatRect(0, 0, SCREEN_WIDTH/SCALE, SCREEN_HEIGHT/SCALE))
window.view = view