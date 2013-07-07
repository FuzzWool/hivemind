#Overriding a (class) instance's method from another class.
import new

class Foo:
	def method_1(self):
		print "old"

	def method_2(self):
	#Call method 1
		self.method_1()

class Barr:
	def __init__(self):
		self.f = Foo()

		def method_3(self):
			print "new"
		self.f.method_2 = \
		 new.instancemethod(method_3, self.f, None)

b = Barr()
b.f.method_2()