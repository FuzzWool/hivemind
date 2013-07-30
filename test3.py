#Testing list getters/setters
class Foo:

	_lst = []
	@property
	def lst(self):
		print "getter"
		return self._lst
	@lst.setter
	def lst(self, arg): print "setter"

f = Foo()

f.lst.append(100)
print f.lst[0]
