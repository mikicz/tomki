# -*- coding: utf-8 -*-
from Literal import Literal
class Insert:
	def __init__(self, ident, value, index):
		self.ident = ident
		self.value = value
		self.index = index
		self.type = "Insert"
	
	def __str__(self):
		return "insert (%s, %s, %s)" % (self.ident, self.value, self.index)

	def run(self, frame, functionFrame):
		self.array = frame.get(self.ident).run(frame, functionFrame)
		self.array.insert(self.index.run(frame, functionFrame), self.value)
		return frame.set(self.ident,Literal(self.array), functionFrame)