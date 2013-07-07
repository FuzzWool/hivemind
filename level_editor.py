import modules as mo
rtrn = mo.KeyTracker(mo.sf.Keyboard.RETURN)
mouse = mo.MyMouse()

def make_grid():
#Make a grid sprite for every tile on the screen.
	grid = []
	grid_dir = "img/level_editor/grid.png"
	tex = mo.sf.Texture.load_from_file(grid_dir)
	x, y = 0, 0
	while x < mo.RENDER_WIDTH:
		while y < mo.RENDER_HEIGHT:
			sprite = mo.MySprite(tex)
			sprite.goto = x, y
			grid.append(sprite)
			y += mo.GRID
		y = 0
		x += mo.GRID
	return grid

class LevelEditor:
	Level = None
	mouse = None

	def __init__(self, Level):
		self.Level = Level
		
		def create_mouse():
			mouse_tex = mo.texture\
			 ("img/level_editor/cursor.png")
			self.mouse = mo.MySprite(mouse_tex)
		create_mouse()

	def loop(self):
	#Draws the cursor in a new position.
		def sround(x, base=mo.GRID):
			return int(base * round(float(x)/base))

		#Grab the mouse cursor and draw it.
		x, y = mo.sf.Mouse.get_position(mo.window)
		x, y = x/mo.SCALE, y/mo.SCALE
		x, y = x - mo.GRID/2, y - mo.GRID/2
		self.mouse.goto = sround(x), sround(y)

	def place_tile(self, x, y):
	#Changes a tile within the level.
		x, y = x/mo.GRID, y/mo.GRID
		x, y = x/mo.SCALE, y/mo.SCALE
		Level.change_tile((x, y), "ab")

	def draw(self):
		self.mouse.draw()

Level = mo.Level("1")
grid = make_grid()
LevelEditor = LevelEditor(Level)
#########################################################
running = True
while running:

	#Logic
	if mo.quit(): running = False
	if rtrn.pressed():
		pass

	if mouse.held():
		LevelEditor.place_tile(*mouse.position())

	LevelEditor.loop()

	#Animation
	#

	#Video
	mo.window.clear(mo.sf.Color.WHITE)
	#
	for s in grid:
		s.draw()
	Level.draw()
	LevelEditor.draw()
	#
	mo.window.display()