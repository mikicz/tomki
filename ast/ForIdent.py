# -*- coding: utf-8 -*-
class ForIdent:
	def __init__(self,name):
		self.name = name
		self.type = "ForIdent"

	def __str__(self):
		return self.name

	def run(self, frame, functionFrame):
		return self.name