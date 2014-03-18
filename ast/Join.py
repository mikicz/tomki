# -*- coding: utf-8 -*-
from Literal import Literal
class Join:
	def __init__(self,array):
		self.array = array
		self.type = "Join"

	def __str__(self):
		ret = "join ( "
		for i in self.array:
			if (ret == "join ( "):
				ret += i.__str__()
			else:
				ret += ", " + i.__str__()
		ret += " )"
		return ret

	def run(self, frame, functionFrame):
		x = []
		for i in self.array:
			y = i.run(frame, functionFrame)
			if (isinstance(y,list)):
				x += y
			else:
				x += [Literal(y)]
		return Literal(x)
