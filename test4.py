#Using GLOBAL to save writing self over and over

class Foo:
	x1, x2, y1, y2 = 1,2,3,4

	@property
	def points(self): s = self; return s.x1,s.y1,s.x2,s.y2

f = Foo()
print f.points