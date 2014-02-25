# -*- coding: utf-8 -*-
class ArrgIdent:
	def __init__(self,name):
		self.name = name
		self.type = "ArrgIdent"

	def __str__(self):
		return self.name

	def run(self, frame, ff):
		return self.name