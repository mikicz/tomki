# -*- coding: utf-8 -*-
class Return:
	def __init__(self,what):
		self.what = what
		self.type = "Return"

	def __str__(self):
		return "return  %s " % (self.what)

	def run(self, frame,ff):
		return self.what.run(frame,None)