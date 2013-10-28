
# Two lists contain instances.
# Choose the instance to be deleted.
# Delete that reference from both lists.

class foo: pass

list1 = []
list2 = []

for i in range(2):
	f = foo()
	list1.append(f)
	list2.append(f); list2.append(f)

print list1
print list2

to_delete = list1[0]
list1 = [item for item in list1 if item != to_delete]
list2 = [item for item in list2 if item != to_delete]

print
print list1
print list2