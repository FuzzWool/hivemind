class pointer:

	def __init__(self):
		self.level_properties = _LevelProperties()

	def controls(self, worldmap, mouse, cursor):
		if mouse.left.double_pressed():
			self._open(worldmap, cursor)
		self._handle()

	#

	def _open(self, worldmap, cursor):
		x,y = cursor.room_position
		if worldmap.in_room_points((x+1,y+1)):
			room = worldmap.rooms[x][y]
			self.level_properties.open(room)

	def _handle(self):
		self.level_properties.handle_events()


from Tkinter import Tk, Frame, Button
from Tkinter import BOTH

from Tkinter import Entry, Label
from Tkinter import N, E, S, W
from Tkinter import INSERT
from Tkinter import LEFT, RIGHT, TOP, BOTTOM
from Tkinter import X, Y
from Tkinter import RAISED

class _LevelProperties:
#Opens and alters the properties of a level,
#with a windows form.
	root = None

	def open(self, Level):
	#Opens the properties window.
	#Passes over the values.
		self.root = Tk()
		self.root.wm_title(Level.graphics.texture_name)
		self.lp1 = \
		self.LevelProperties_1(self.root, Level)

		def save():
			tileset = self.lp1.tileset.get()
			Level.change_texture(tileset)
			self.root.destroy()

		self.butt = \
		self.ConfirmButtons(self.root, save)
		self.lp1.focus_force()
		self.root.mainloop()

	def handle_events(self):
	#Updates only windows within existence.
		if self.root != None:
			if len(self.root.children) >= 1:
				tkinter_open = True
			else:
				tkinter_open = False
		else:
			tkinter_open = False

		if tkinter_open:
			if len(self.root.children) >= 1:
				self.root.update()

	#

	class MyFrame(Frame):
	#Override me!
		def __init__(self, parent, arg=None):
			Frame.__init__(self, parent)
			self.parent = parent
			self.initUI(arg)

		def initUI(self, arg=None):
		#Replace me!
			pass

	class LevelProperties_1(MyFrame):

		def initUI(self, Level):
		#Level Properties title
			# name = Level.name
			tileset = Level.graphics.texture_name

			entry_row = 1
			Ltileset = Label(self, text="Tileset")
			Ltileset.grid(row=entry_row, column=0)
			Etileset = Entry(self)
			Etileset.grid(row=entry_row, column=1)
			Etileset.insert(INSERT, tileset)

			self.pack(fill=BOTH, expand=1)

			self.tileset = Etileset

	class ConfirmButtons(MyFrame):

		def initUI(self, arg=None):
			frame = Frame(self, relief=RAISED,\
			 borderwidth=1)
			frame.pack(fill=BOTH, expand=1)

			Bclose = Button(self, text="Nah.",\
			 command=self.parent.destroy)
			Bclose.pack(side=RIGHT, padx=5, pady=5)
			Bok = Button(self, text="Okay!", command=arg)
			Bok.pack(side=RIGHT)

			self.pack(fill=BOTH, expand=1)