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
		array = frame.get(self.ident).run(frame, functionFrame)
		array.append(self.value.run(frame, functionFrame))
		return frame.set(self.ident,Literal(array), functionFrame)