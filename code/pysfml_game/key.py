from code.pysfml_game.window import sf

class KeyTracker:
#Tracks whether or not a key is pressed or held.
#May be locked or unlocked externally.

# * Requires reset_keys call every loop.


	def __init__ (self, key):
		self.init_class()

		self.key = key
		self.was_pressed = False


	# INSTANCE TRACKING
	__all__ = set()
	def init_class(self): self.__class__.__all__.add(self)


	# BASIC EVENTS (w/ locking)
	
	def held(self):
		return sf.Keyboard.is_key_pressed(self.key)

	def pressed(self):
		pressed = False
		if not self.was_pressed and self.held():
			pressed = True
		else: pressed = False

		return pressed

	def _reset(self):
		"""To be called as part of a global loop."""
		self.was_pressed = self.held()


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


def reset_all():
	for i in KeyTracker.__all__: i._reset()
