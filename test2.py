class Foo(object):
	
	facing_left = False
	@property
	def facing_right(self):
		return not self.facing_left

	@facing_right.setter
	def facing_right(self, arg):
		self.facing_left = not arg




f = Foo()

print f.facing_left, f.facing_right
f.facing_left = True
print f.facing_left, f.facing_right
f.facing_right = True
print f.facing_left, f.facing_right
