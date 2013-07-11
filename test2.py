foo = [range(3) for i in range(3)]

print foo

for fi, f in enumerate(foo):
	foo[fi] = [None] + foo[fi]

print foo