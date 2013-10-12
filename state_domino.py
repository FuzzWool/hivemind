#Make a STATE DOMINO.

class state_domino(object):
#When the domino falls, so do those before it.
#FALSE all the states before a TRUE domino.

	def __init__(self, truth):
		self.state = truth


	def dominos_before(self, dominos):
		self._dominos_before = dominos

		#Every domino before it is given the rest,
		#recursed until the very last domino.
		if len(dominos) > 0:
			dominos[-1].dominos_before(dominos[:-1])


	def __call__(self, truth=None):
		if truth == None: return self.state

		self.state = truth
		if truth == True:
			for state in self._dominos_before:
				state(False)

	def all_false(self):
		truth = True
		for state in self._dominos_before + [self]:
			if state() == True:
				truth = False
		return truth


dominos = []
for i in range(5):
	domino = state_domino(False)
	dominos.append(domino)

dominos[-1].dominos_before(dominos[:-1])

# for domino in dominos:
# 	print domino._dominos_before

# dominos[3](True)

# for domino in dominos:
# 	print domino()


print dominos[-1].all_false()