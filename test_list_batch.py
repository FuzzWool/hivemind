
def read_list(used_list):
#Read a 2D list as a human-readable table.
	yx_list = []
	w = len(used_list)
	h = len(used_list[0])

	#Convert list to YX FORMAT.
	for y in range(h):
		yx_list.append([])
		for x in range(w):
			cell = used_list[x][y]
			yx_list[-1].append(cell)

	#READ IT.
	for x in yx_list:
		print x

###


#Stitch together the 2D lists.
#up to down (left to right is easy)

def list_yx(use_list):
#Change a list from an XY format to a YX format.
	w, h = len(use_list), len(use_list[0])
	new_list = []
	for y in range(h):
		new_list.append([])

		for x in range(w):
			new_list[-1].append(use_list[x][y])

	return new_list


room1 = [[0,0],[1,0],[2,0],[3,0]]
room2 = [[4,0],[5,0],[6,0],[7,0]]
room3 = [[0,1],[1,1],[2,1],[3,1]]
room4 = [[4,1],[5,1],[6,1],[7,1]]
worldmap = [[room1, room3], [room2, room4]]


#The WorldMap has access to ALL of the tiles.
#ALL of the tiles from EVERY ROOM.

#All the ROOM COLUMNS.
#All the TILE COLUMNS from EVERY ROOM.
#Attach them to TILES.


tiles = []
#map column
for map_x in worldmap:
	
	#nab every tile...
	w = len(map_x[0])
	for tile_x in range(w):

		#...from every room.
		column = []
		for map_y in map_x:
			column += map_y[tile_x]
		
		tiles.append(column)

for i in list_yx(tiles): print i