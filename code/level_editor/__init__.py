from tools import *

#

from code.pysfml_game import MyTexture, MySprite

#ui
from code.pysfml_game import SCREEN_HEIGHT
from code.pysfml_game import GRID
from code.pysfml_game import sf
from code.pysfml_game import window


# ####
#ENTITY TOOLS
opted_entities = []
def e(append): opted_entities.append(append)
#
e("tile_key")
e("tile_lock")

# ####

class toolbox:
	
	def __init__(self, worldmap, entities):
		self.ui = ui()
		self._init_cursor()
		#
		self.pointer = pointer()
		self.tile = tile()
		self.camera = camera(worldmap)

		#Entities
		self.entity = entity(entities, "tile_key")


	def draw(self, camera, mouse):
		self._move_cursor(camera, mouse)

		if self.ui.selected == "tile":
			self.tile.draw()
			self.cursor.draw()
		if self.ui.selected == "camera":
			self.camera.draw(camera)

		#Entities
		if self.ui.selected in opted_entities:
			self.cursor.draw()
			self.entity.draw()



	def static_draw(self):
		self.ui.draw()

	def controls(self, entities, worldmap,\
	 camera, mouse, key):

		#Save
		if key.L_CTRL.held():
			if key.S.pressed():
				print "====SAVING==="
				worldmap.save()
				entities.save()
				print "============="

		#Move the camera
		else:
			if key.A.held(): camera.x -= GRID
			if key.D.held(): camera.x += GRID
			if key.W.held(): camera.y -= GRID
			if key.S.held(): camera.y += GRID

		#Toolbox buttons
		self.ui.controls(mouse)

		#Tool controls
		if not self.ui.is_hovering(mouse):

			if self.ui.selected == "pointer":
				self.pointer.controls\
				(worldmap, mouse, self.cursor)
			
			if self.ui.selected == "tile":
				self.tile.controls\
				(worldmap, mouse, key, self.cursor)

			if self.ui.selected == "camera":
				self.camera.controls\
				(worldmap, mouse, self.cursor)

			#Entities
			if self.ui.selected in opted_entities:
				self.entity.name = self.ui.selected
				self.entity.controls(mouse,self.cursor)

	#



	#cursor
	def _init_cursor(self): #init
		cursor_tex \
		= MyTexture("assets/level_editor/cursor.png")
		self.cursor = MySprite(cursor_tex)

	def _move_cursor(self, camera, mouse): #draw
		x,y = mouse.tile_position
		x += camera.tile_x
		y += camera.tile_y
		self.cursor.tile_position = x,y
	#




class ui: #toolbox
#An interface for selecting tools.

	def __init__(self):
		self.selected = None

		self._init_menu()
		self._init_icons()
		

	def controls(self, mouse):

		if self.is_hovering(mouse):
			if mouse.left.pressed():
				self._select(mouse)

	def draw(self):
		window.draw(self.menu)

		for column in self.icons:
			for icon in column:
				if icon != None:
					icon.draw()

	#

	#controls, _init_icons
	def _select(self, mouse=None, x=0, y=0):
		if mouse != None:
			x,y = mouse.tile_position
		self._transparent_icons()
		self.icons[x][y].opaque()
		self.selected = self.icons[x][y].tool


	#controls, _controls
	def is_hovering(self, mouse):
		x,y = mouse.x, mouse.y
		if 0 <= x <= 50\
		and 0 <= y <= SCREEN_HEIGHT:
			return True
		return False

	#

	def _init_menu(self):
		w, h = 50, SCREEN_HEIGHT
		self.menu = sf.RectangleShape((w,h))

	def _init_icons(self):
		self.icons = []

		#Empty
		w, h = 50, SCREEN_HEIGHT
		w, h = int(w/GRID),int(h/GRID)
		for x in range(w):
			self.icons.append([])
			for y in range(h):
				_icon = icon()
				_icon.x, _icon.y = x*GRID, y*GRID
				self.icons[-1].append(_icon)
		#

		#Tools
		self.icons[0][0].tool = "pointer"
		self.icons[1][0].tool = "tile"
		self.icons[0][1].tool = "camera"

		#Entities
		self.icons[0][4].tool = "tile_key"
		self.icons[1][4].tool = "tile_lock"


		#default
		self._select(x=1,y=0)


	def _transparent_icons(self): #init_icons, select
		for x in self.icons:
			for y in x:
				y.transparent()


class icon(object): #toolbox.ui
	texture = MyTexture("assets/level_editor/toolbox.png")

	def __init__(self):
		self.sprite = MySprite(self.texture)
		self.sprite.clip.set(25,25)
		self.transparent()

	def draw(self):
		self.sprite.draw()

	def transparent(self):
		self.sprite.color = sf.Color(255,255,255,100)
	def opaque(self):
		self.sprite.color = sf.Color(255,255,255,255)


	#
	_tool = None
	@property
	def tool(self): return self._tool
	@tool.setter
	def tool(self, name):
		self._tool = name
		if name == "pointer": self.sprite.clip.use(1,0)
		if name == "tile": self.sprite.clip.use(2,0)
		if name == "camera": self.sprite.clip.use(3,0)

		#Entities
		if name == "tile_key": self.sprite.clip.use(5,0)
		if name == "tile_lock": self.sprite.clip.use(6,0)

	#

	@property
	def x(self): return self.sprite.x
	@x.setter
	def x(self, x): self.sprite.x = x

	@property
	def y(self): return self.sprite.y
	@y.setter
	def y(self, y):
		self.sprite.y = y