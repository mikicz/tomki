# -*- coding: utf-8 -*-
from Literal import Literal
class Pop:
	def __init__(self, ident, index):
		self.ident = ident
		self.index = index
		self.type = "Pop"

	def __str__(self):
		return "pop (%s, %s)" % (self.ident, self.index)

	def run(self, frame, ff):
		self.array = frame.get(self.ident).run(frame,ff)
		self.value = self.array.pop(self.index.run(frame, ff))
		frame.set(self.ident,Literal(self.array), ff)
		return Literal(self.value.run(frame,ff))