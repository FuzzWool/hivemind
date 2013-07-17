
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

class _LevelProperties:
#Opens and alters the properties of a level,
#with a windows form.
	root = None

	def open(self, Level):
	#Opens the properties window.
	#Passes over the values.
		self.root = Tk()
		self.app = self._frame(self.root, Level)
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
	#All the tkinter design settings.

		def __init__(self, parent, Level):
			Frame.__init__(self, parent)   
			 
			self.parent = parent        
			self.initUI(Level)
			
		def initUI(self, Level):

			title = "'%s' Properties" % Level.name
			self.parent.title(title)
			self.pack(fill=BOTH, expand=1)

			x, y = Level.room_x, Level.room_y
			w, h = Level.room_w, Level.room_h
			self.Level = Level

			pad = 10
			for ix in range(4):
				self.columnconfigure(ix, pad=pad/2)
			for iy in range(4):
				self.rowconfigure(iy, pad=pad*2)

			#Room Position/Size Entry
			Lx = Label(self, text="room x")
			Lx.grid(row=0, column=0)
			Ex = Entry(self, width=10)
			Ex.insert(INSERT, x)
			Ex.grid(row=0, column=1)

			Ly = Label(self, text="room y")
			Ly.grid(row=0, column=2)
			Ey = Entry(self, width=10)
			Ey.insert(INSERT, y)
			Ey.grid(row=0, column=3)

			Lw = Label(self, text="room w")
			Lw.grid(row=1, column=0)
			Ew = Entry(self, width=10)
			Ew.insert(INSERT, w)
			Ew.grid(row=1, column=1)

			Lh = Label(self, text="room h")
			Lh.grid(row=1, column=2)
			Eh = Entry(self, width=10)
			Eh.insert(INSERT, h)
			Eh.grid(row=1, column=3)
			#

			#Confirmation Buttons
			ok = Button(self, text="Okay!", \
				command=self.save_results)
			ok.grid(sticky=N+E+S+W, row=2, column=2)

			no = Button(self, text="NO.",\
				command=self.parent.destroy)
			no.grid(sticky=N+E+S+W, row=2, column=3)

			#Texture changing
			text = Level.texture_name
			#
			Ltex = Label(self, text="Texture")
			Ltex.grid(row=3, column=1)
			Etex = Entry(self, width=20)
			Etex.insert(INSERT, text)
			Etex.grid(row=3, column=2)


			self.pack
			self.x = Ex; self.y = Ey
			self.w = Ew; self.h = Eh
			#
			self.tex = Etex

		def save_results(self):
			self.Level.room_x = int(self.x.get())
			self.Level.room_y = int(self.y.get())
			self.Level.room_w = int(self.w.get())
			self.Level.room_h = int(self.h.get())
			#
			self.Level.change_texture(self.tex.get())

			self.grid_forget()
			self.parent.destroy()