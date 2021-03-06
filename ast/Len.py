# -*- coding: utf-8 -*-
from Literal import Literal
class Len:
	def __init__(self, ident):
		self.ident = ident
		self.type = "Len"

	def __str__(self):
		return "len (%s)" % (self.ident, )

	def run(self, frame, functionFrame):
		self.array = frame.get(self.ident).run(frame, functionFrame)
		self.value = len(self.array)
		return Literal(self.value)