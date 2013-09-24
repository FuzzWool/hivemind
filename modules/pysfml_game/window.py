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

video_mode = sf.VideoMode(SCREEN_WIDTH, SCREEN_HEIGHT)
window = sf.RenderWindow(video_mode, "Hivemind")
# window.framerate_limit = 1
window.vertical_synchronization = True

del scale

RENDER_CENTER = (RENDER_WIDTH/2, RENDER_HEIGHT/2)