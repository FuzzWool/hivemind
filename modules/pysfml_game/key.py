from modules.pysfml_game.window import sf

#Tracks whether or not a key is pressed, held, and the intervals it is held for.
class KeyTracker:
	def __init__ (self, key):
		self.key = key
		self.was_pressed = False

		self.timer = sf.Clock()
		self.secs_interval = 0
		self.intervals = 0
		self.old_secs_interval = self.secs_interval

	#Basic Events
	
	def held(self):
		return sf.Keyboard.is_key_pressed(self.key)

	def pressed(self):
		pressed = False
		if not self.was_pressed and self.held(): pressed = True
		else: pressed = False

		self.was_pressed = self.held()
		return pressed

	# #Time-based Events

	# def hit_interval(self):
	# 	if self.timer.elapsed_time.as_seconds() >= self.secs_interval:
	# 		self.intervals += 1
	# 		self.timer.restart(); return True
	# 	return False

	# def decrease_interval(self):
	# 	if self.held() \
	# 	and self.intervals >= 10 and self.secs_interval >= 0.01:
	# 		self.secs_interval *= 0.50; self.intervals = 0

	# def set_interval(self, interval): self.secs_interval = interval; self.old_secs_interval = interval
	# def reset_interval(self): self.secs_interval = self.old_secs_interval

	# def intervally_held(self):
	# 	if self.pressed(): self.timer.restart(); return True
	# 	if self.hit_interval() and self.held(): self.decrease_interval(); return True
	# 	if self.held() == False: self.reset_interval()
	# 	else: return False


#Create KeyTrackers for all of the sf.Keyboard keys.
for i in sf.Keyboard.__dict__:
	if i != "is_key_pressed" \
	and i[:2] != "__":
		v = sf.Keyboard.__dict__[i]
		name = i
		if name == "L_CONTROL":
			name = "L_CTRL"
		if name == "R_CONTROL":
			name = "R_CTRL"
		vars()[name] = KeyTracker(v)