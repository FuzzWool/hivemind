from Tkinter import Tk, Frame, Button
from Tkinter import BOTH

from Tkinter import Entry, Label
from Tkinter import N, E, S, W
from Tkinter import INSERT
from Tkinter import LEFT, RIGHT, TOP, BOTTOM
from Tkinter import X, Y
from Tkinter import RAISED

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

	def initUI(self, arg=None):
	#Level Properties title
		name = "Me!"
		tileset = "The best!"

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

	def initUI(self, arg=None):
	#Position/Size Labels
		x, y = 0, 1
		w, h = 2, 3

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


root = Tk()
lp1 = LevelProperties_1(root)
lp2 = LevelProperties_2(root)

def save():
	print int(lp2.x.get())
	root.destroy()

butt = ConfirmButtons(root, save)
lp1.focus_force()
root.mainloop()