# -*- coding: utf-8 -*-
class Print:
	def __init__(self,what):
		self.what = what
		self.type = "Print"

	def __str__(self):
		return "print ( %s )" % (self.what)

	def run(self, frame,ff):
		print self.what.run(frame,None)