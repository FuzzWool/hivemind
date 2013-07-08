import modules as mo

class EditMouse(mo.MyMouse):

	def grid_position(self):
	#Return the grid position of the mouse.
		x, y = self.position()
		x /= mo.GRID
		y /= mo.GRID
		return x, y