from code.pysfml_game.window import sf

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