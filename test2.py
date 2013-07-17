#Look for a text document by name.
#If it doesn't exist, make a new one.

#Try making a new text document from scratch.

# f = open("outside/levels/"+level_dir+".txt")
# level = f.read()
# f.close()

# #Save it to the original file.
# f = open("outside/levels/"+self.name+".txt", "r+")
# f.write(text)
# f.close()

level_dir = "outside/levels/three.txt"
try:
	level = open(level_dir)
	print "Loaded."
except:
	print "Didn't load. Made a new file."
	level = open(level_dir, "w")