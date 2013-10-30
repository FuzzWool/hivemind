from code.game.entities.entity import entity

class timer_start(entity):

	def react(self):
		if self.in_points(self.Player.cbox):
			self.Timer.start()