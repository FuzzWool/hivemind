class C1:
	def __init__(self):
		self.b = False


class C2(object):
	def __init__(self, _c1):
		self._c1 = _c1

	@property
	def b(self):
		b = self._c1.b
		return b
	@b.setter
	def b(self, truth):
		self._c1.b = truth

	def set_false(self):
		self.b = False
	


c1 = C1()
c2 = C2(c1)

print c1.b
print c2.b

print "***"
c1.b = True

print c1.b
print c2.b

c2.set_false()