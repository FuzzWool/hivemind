#Generate generic alphabet for the collision tilemap.

from modules.game import Room
alphabet = Room.alphabet

text = ""
for x in range(8):
	for y in range(13):
		c1 = alphabet[y]
		c2 = alphabet[x]
		text = text + c1+c2
	text += "\n"

print text