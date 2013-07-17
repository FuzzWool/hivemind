
class Pointer:
#A tool designed for examining and altering other objects'
#properties.
	
	def __init__(self):
		self.LevelProperties = _LevelProperties()


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
		self.lp1 = self.LevelProperties_1(self.root, Level)
		self.lp2 = self.LevelProperties_2(self.root, Level)

		def save():
			name = self.lp1.name.get()
			tileset = self.lp1.tileset.get()
			x = int(self.lp2.x.get())
			y = int(self.lp2.y.get())
			w = int(self.lp2.w.get())
			h = int(self.lp2.h.get())

			if name != "WorldMap":
				Level.name = name
			else:
				print "Cannot name file 'WorldMap'."
			Level.change_texture(tileset)
			Level.room_x = x; Level.room_y = y
			Level.room_w = w; Level.room_h = h

			self.root.destroy()

		self.butt = self.ConfirmButtons(self.root, save)
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
			name = Level.name
			tileset = Level.texture_name

			entry_row = 0
			Lname = Label(self, text="Name")
			Lname.grid(row=entry_row, column=0)
			Ename = Entry(self)
			Ename.grid(row=entry_row, column=1)
			Ename.insert(INSERT, name)

			entry_row = 1
			Ltileset = Label(self, text="Tileset")
			Ltileset.grid(row=entry_row, column=0)
			Etileset = Entry(self)
			Etileset.grid(row=entry_row, column=1)
			Etileset.insert(INSERT, tileset)

			self.pack(fill=BOTH, expand=1)

			self.name = Ename
			self.tileset = Etileset

	class LevelProperties_2(MyFrame):

		def initUI(self, Level):
		#Position/Size Labels
			x, y = Level.room_x, Level.room_y
			w, h = Level.room_w, Level.room_h

			entry_width = 10
			entry_row = 0

			Lx = Label(self, text="x", width=2)
			Lx.grid(row=entry_row, column=0)
			Ex = Entry(self, width=entry_width)
			Ex.insert(INSERT, x)
			Ex.grid(row=entry_row, column=1)

			Ly = Label(self, text="y")
			Ly.grid(row=entry_row, column=2)
			Ey = Entry(self, width=entry_width)
			Ey.insert(INSERT, y)
			Ey.grid(row=entry_row, column=3)

			entry_row = 1

			Lw = Label(self, text="w")
			Lw.grid(row=entry_row, column=0)
			Ew = Entry(self, width=entry_width)
			Ew.grid(row=entry_row, column=1)
			Ew.insert(INSERT, w)

			Lh = Label(self, text="h")
			Lh.grid(row=entry_row, column=2)
			Eh = Entry(self, width=entry_width)
			Eh.grid(row=entry_row, column=3)
			Eh.insert(INSERT, h)

			self.pack(fill=BOTH, expand=1)

			self.x, self.y = Ex, Ey
			self.w, self.h = Ew, Eh

	class ConfirmButtons(MyFrame):

		def initUI(self, arg=None):
			frame = Frame(self, relief=RAISED, borderwidth=1)
			frame.pack(fill=BOTH, expand=1)

			Bclose = Button(self, text="Nah.", command=self.parent.destroy)
			Bclose.pack(side=RIGHT, padx=5, pady=5)
			Bok = Button(self, text="Okay!", command=arg)
			Bok.pack(side=RIGHT)

			self.pack(fill=BOTH, expand=1)