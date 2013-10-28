# ABSTRACT
# Designed to ID individual entities.

# * Each instance of a sub-class is listed.
# * Each new instance of a sub-class has an
# incremented ID.


###############################################

# # For each new class created, increment it's ID.
# # SUCCESS


# class foo:
# 	id = 0

# 	def __init__(self):
# 		self.id = foo.id
# 		foo.id += 1

# foos = []
# for i in range(5):
# 	foos.append(foo())

# for foo in foos: print foo.id


###############################################

# # For each new class created, increment it's ID.
# # The ID is located inside of a virtual class.
# # For each of it's children, update it's own ID.
# # FAILURE

# class _foo:
# 	id = 0
# 	def __init__(self): self.id = _foo.id; _foo.id += 1

# class f1(_foo): pass
# class f2(_foo): pass

# a = f1()
# b = f1()
# c = f1()
# d = f2()
# e = f2()
# f = f1()
# g = f2()

# foos = [a,b,c,d,e,f,g]

# for foo in foos:
# 	print foo.id


####1
# _foo contains a list of instances inherited from it.
#2 - Add instances (by class name) to a dictionary

class _foo:
#Contain every instance inherited from it.
	__all__ = {}
	id = 0

	def __init__(self):
		self._contain_instance()
		self._get_id()

	def _contain_instance(self):
		name = self.__class__.__name__
		try:
			_foo.__all__[name].append(self)
		except:
			_foo.__all__[name] = [self]

	def _get_id(self):
		name = self.__class__.__name__
		self.id = len(_foo.__all__[name])


class f1(_foo): pass
class f2(_foo): pass
class f3(_foo): pass

a = f1()
b = f1()
c = f1()
d = f2()
e = f1()
f = f3()
g = f2()


foos = [a,b,c,d,e,f,g]
for foo in foos:
	print foo.id


####2
# Add instances by name to a dictionary.

# names = {}

# def add(name, item):
# 	try: names[name].append(item)
# 	except: names[name] = [item]

# add("tree", "oak")
# add("tree", "pine")

# add("cat","fluffy")

# print names["tree"]