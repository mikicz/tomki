# -*- coding: utf-8 -*-
from Literal import Literal
class Append:
	def __init__(self, ident, value):
		self.ident = ident
		self.value = value
		self.type = "Append"

	def __str__(self):
		return "append (%s, %s)" % (self.ident, self.value)

	def run(self, frame, functionFrame):
		self.array = frame.get(self.ident).run(frame, functionFrame)
		self.array.append(self.value)
		return frame.set(self.ident,Literal(self.array), functionFrame)