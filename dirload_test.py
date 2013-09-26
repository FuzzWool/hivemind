import glob
import os

# Open all the TXT FILES in a directory.
# Store it in a DICT. Keys for filename, file data retrieved.

directory = "_temptest"
os.chdir(directory)
files = {}
for filename in glob.glob("*.txt"):
	read_file = open(filename).read()
	files[filename] = read_file
os.chdir("../")

print files
print os.getcwd()