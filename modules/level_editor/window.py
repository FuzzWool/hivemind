import modules as mo

# #Window adjustments for the level_editor's usage.
mo.SCALE = 1
mo.GRID = 25

mo.SCREEN_WIDTH = 400 * mo.SCALE * 2
mo.SCREEN_HEIGHT = 300 * mo.SCALE * 2
mo.RENDER_WIDTH = mo.SCREEN_WIDTH / mo.SCALE
mo.RENDER_HEIGHT = mo.SCREEN_HEIGHT / mo.SCALE

mo.window.create(
	mo.sf.VideoMode\
	 (mo.SCREEN_WIDTH, mo.SCREEN_HEIGHT), "Hivemind - Level Editor")
mo.window.framerate_limit = 60
mo.window.vertical_sync_enabled = True

view = mo.sf.View.from_rect(\
	mo.sf.FloatRect(0, 0, mo.SCREEN_WIDTH/mo.SCALE, mo.SCREEN_HEIGHT/mo.SCALE))
mo.window.view = view

#Update Camera.
mo.Camera._ = mo.window.view
mo.Camera.zoom = mo.SCALE