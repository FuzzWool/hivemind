import modules as mo

class EditMouse(mo.MyMouse):

	def grid_position(self, Camera=None):
	#Return the grid position of the mouse.
		x, y = self.position(Camera)
		x /= mo.GRID
		y /= mo.GRID
		return x, y