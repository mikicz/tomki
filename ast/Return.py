# -*- coding: utf-8 -*-
from Literal import Literal
class Return:
	def __init__(self, what):
		self.what = what
		self.type = "Return"

	def __str__(self):
		return "return  %s " % (self.what)

	def run(self, frame, functionFrame):
		raise Literal(self.what.run(frame, functionFrame))