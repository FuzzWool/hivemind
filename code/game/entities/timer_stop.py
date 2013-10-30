from code.game.entities.entity import entity


class timer_stop(entity):

	def react(self):
		if self.in_points(self.Player.cbox):
			self.Timer.stop()