from Tkinter import Tk, Frame, Button
from Tkinter import BOTH

from Tkinter import Entry, Label
from Tkinter import N, E, S, W
from Tkinter import INSERT

class LevelProperties:
#Handles a Tkinter window.
	root = None

	def open(self):
		self.root = Tk()
		self.app = self._frame(self.root)
		self.app.focus_force()

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

	class _frame(Frame):

		def __init__(self, parent):
			Frame.__init__(self, parent)   
			 
			self.parent = parent        
			self.initUI()
			
		def initUI(self):

			self.parent.title("Level Properties")
			self.pack(fill=BOTH, expand=1)

			x, y, w, h = 1, 2, 3, 4

			pad = 10
			for ix in range(4):
				self.columnconfigure(ix, pad=pad/2)
			for iy in range(3):
				self.rowconfigure(iy, pad=pad*2)

			Lx = Label(self, text="x")
			Lx.grid(row=0, column=0)
			Ex = Entry(self, width=10)
			Ex.insert(INSERT, x)
			Ex.grid(row=0, column=1)

			Ly = Label(self, text="y")
			Ly.grid(row=0, column=2)
			Ey = Entry(self, width=10)
			Ey.insert(INSERT, y)
			Ey.grid(row=0, column=3)

			Lw = Label(self, text="w")
			Lw.grid(row=1, column=0)
			Ew = Entry(self, width=10)
			Ew.insert(INSERT, w)
			Ew.grid(row=1, column=1)

			Lh = Label(self, text="h")
			Lh.grid(row=1, column=2)
			Eh = Entry(self, width=10)
			Eh.insert(INSERT, h)
			Eh.grid(row=1, column=3)

			ok = Button(self, text="Okay!", \
				command=self.print_results)
			ok.grid(sticky=N+E+S+W, row=2, column=2)

			no = Button(self, text="NO.",\
				command=self.parent.destroy)
			no.grid(sticky=N+E+S+W, row=2, column=3)

			self.pack
			self.x = Ex; self.y = Ey
			self.w = Ew; self.h = Eh

		def print_results(self):
			print self.x.get(), self.y.get(),\
					self.w.get(), self.h.get()
			self.parent.destroy()