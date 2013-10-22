#Class gains the properties of another class.


class Foo:
	def __init__(self):
		self.a = 0
		self.b = 0
		self.c = 0

f1 = Foo()
f2 = Foo()

f1.a = 1
f1.b = 1

f2.c = 2

f2 = f1

print f1.a, f1.b, f1.c
print f2.a, f2.b, f2.c