# -*- coding: utf-8 -*-
from Literal import Literal
class Pop:
	def __init__(self, ident, index):
		self.ident = ident
		self.index = index
		self.type = "Pop"

	def __str__(self):
		return "pop (%s, %s)" % (self.ident, self.index)

	def run(self, frame,  functionFrame):
		array = frame.get(self.ident).run(frame, functionFrame)
		value = array.pop(self.index.run(frame,  functionFrame))
		frame.set(self.ident, Literal(array), functionFrame)
		return Literal(value.run(frame, functionFrame))