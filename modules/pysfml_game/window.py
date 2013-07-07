import sfml as sf

SCALE = 1

SCREEN_WIDTH = 400 * SCALE
SCREEN_HEIGHT = 300 * SCALE
window = sf.RenderWindow(sf.VideoMode(SCREEN_WIDTH, SCREEN_HEIGHT), "Hivemind")
window.framerate_limit = 60
window.vertical_sync_enabled = True

view = sf.View.from_rect(\
	sf.FloatRect(0, 0, SCREEN_WIDTH/SCALE, SCREEN_HEIGHT/SCALE))
window.view = view

GRID = 25
RENDER_WIDTH = SCREEN_WIDTH / SCALE
RENDER_HEIGHT = SCREEN_HEIGHT / SCALE