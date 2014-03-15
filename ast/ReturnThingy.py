# -*- coding: utf-8 -*-
class ReturnThingy:
	def __init__(self, value):
		self.value = value
		self.type = "ReturnThingy"

	def __str__(self):
		return self.value.__str__()

	def run(self, frame, ff):
		return self.value.run(frame,ff)