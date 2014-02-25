# -*- coding: utf-8 -*-
class FunctionIdent:
	def __init__(self,name):
		self.name = name
		self.type = "FunctionIdent"

	def __str__(self):
		return self.name

	def run(self, frame,ff):
		return self.name