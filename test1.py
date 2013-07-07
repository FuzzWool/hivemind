y = 3
foo = [None for i in range(y)]
barr = []
for i in range(3):
	barr.append(foo[:])

print barr