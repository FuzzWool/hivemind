from code.pysfml_game import MyCamera
from code.pysfml_game import physics_animation
from code.pysfml_game import ROOM_WIDTH, ROOM_HEIGHT

class GameCamera(MyCamera):
# * Obeys Camera Locks.
# * Smoothly animates between rooms.

	def __init__(self):
		MyCamera.__init__(self)

		self.focus = self #The object to focus on.

		self.animation_x = physics_animation()
		self.animation_y = physics_animation()


	def process_movement(self, worldmap):
	#Follow the focus, stay within bounds.

		#Follow focus
		# > _obey_camera_locks

		#Stop at locks
		x,y = self.focus.room_center
		room = worldmap.rooms[x][y]

		self._obey_camera_locks(room)

		#Animate past locks
		self.x1 += self.animation_x.play(self.x1)
		self.y1 += self.animation_y.play(self.y1)


	def _obey_camera_locks(self, room):
	#Obey the camera locks the focused object is in.

		#Find lock points.
		x1,y1,x2,y2 = None, None, None, None
		if room.camera_locks.left: x1 = room.x1
		if room.camera_locks.right: x2 = room.x2
		if room.camera_locks.up: y1 = room.y1
		if room.camera_locks.down: y2 = room.y2


		#LOCKS
		#Keep in lock boundaries.
		#Smoothly animate if gone outside.

		f = 8

		#If any, keep within the bounds.
		if x1 != None and self.x1 < x1:
			self.animation_x.end = x1
			self.animation_x.speed_by_frames(self.x, f)

		if x2 != None and self.x2 > x2:
			self.animation_x.end = x2-ROOM_WIDTH
			self.animation_x.speed_by_frames(self.x, f)

		if y1 != None and self.y1 < y1:
			self.animation_y.end = y1
			self.animation_y.speed_by_frames(self.y, f)

		if y2 != None and self.y2 > y2:
			self.animation_y.end = y2-ROOM_HEIGHT
			self.animation_y.speed_by_frames(self.y, f)

		#FOLLOW
		#Follow the focus, but obey lock boundaries.
		#If the offset misses the mark, seal it.

		old_center = self.center
		self.center = self.focus.center[0], self.center[1]

		if x1 != None and self.x1 <= x1:
			self.center = old_center
			if self.x1 > x1: self.x1 = x1

		if x2 != None and self.x2 >= x2:
			self.center = old_center
			if self.x2 < x2: self.x2 = x2
		
		old_center = self.center
		self.center = self.center[0], self.focus.center[1]

		if y1 != None and self.y1 <= y1:
			self.center = old_center
			if self.y1 > y1: self.y1 = y1

		if y2 != None and self.y2 >= y2:
			self.center = old_center
			if self.y2 < y2: self.y2 = y2