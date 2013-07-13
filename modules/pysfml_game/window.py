import sfml as sf

scale = 2
GRID = 25

RENDER_WIDTH = 600
RENDER_HEIGHT = 300
SCREEN_WIDTH = RENDER_WIDTH * scale
SCREEN_HEIGHT = RENDER_HEIGHT * scale 

ROOM_SIZE = [RENDER_WIDTH, RENDER_HEIGHT]
ROOM_WIDTH = ROOM_SIZE[0]
ROOM_HEIGHT = ROOM_SIZE[1]


window = \
	sf.RenderWindow(\
		sf.VideoMode\
		 (SCREEN_WIDTH, SCREEN_HEIGHT), "Hivemind")
window.framerate_limit = 60
window.vertical_sync_enabled = True

del scale