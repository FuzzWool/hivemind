from Tkinter import Tk, Frame, Button
from Tkinter import BOTH

from Tkinter import Entry, Label
from Tkinter import N, E, S, W
from Tkinter import INSERT
from Tkinter import LEFT, RIGHT, TOP, BOTTOM
from Tkinter import X, Y

class MyFrame(Frame):
#Override me!
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()

	def initUI(self):
	#Replace me!
		pass

class LevelProperties_title(MyFrame):
#All the tkinter design settings.

	def initUI(self):
		#Level Properties title
		title = "Level Properties (in Rooms)"
		Ltitle = Label(self, text=title)
		Ltitle.pack()

		self.pack(fill=BOTH, expand=1)

class LevelProperties(MyFrame):
#All the tkinter design settings.
		
	def initUI(self):
		entry_w = 10
		entry_row = 0

		#Position/Size Labels
		Lx = Label(self, text="x", width=2)
		Lx.grid(row=entry_row, column=0)
		Ex = Entry(self, width=entry_w)
		Ex.insert(INSERT, "woah")
		Ex.grid(row=entry_row, column=1)

		Ly = Label(self, text="y")
		Ly.grid(row=entry_row, column=2)
		Ey = Entry(self, width=entry_w)
		Ey.insert(INSERT, "filler")
		Ey.grid(row=entry_row, column=3)

		self.pack(fill=BOTH, expand=1)


root = Tk()
app1 = LevelProperties_title(root)
app2 = LevelProperties(root)
app1.focus_force()
root.mainloop()