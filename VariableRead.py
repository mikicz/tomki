# -*- coding: utf-8 -*-
class VariableRead:
	""" Cteni hodnoty ulozene v promenne. """
	def __init__(self, variableName):
		self.variableName = variableName
		self.type = "variableRead"

	def __str__(self):
		return self.variableName

	def run(self,frame,ff):
		return frame.get(self.variableName).run(frame,ff)