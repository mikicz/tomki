# -*- coding: utf-8 -*-
class VariableWrite:
	""" Zapis hodnoty do promenne. Krom nazvu promenne si pamatuje i vyraz, kterym se vypocita hodnota. """
	def __init__(self, variableName, value):
		self.variableName = variableName
		self.value = value
		self.type = "variableWrite"

	def __str__(self):
		return "%s = %s" % (self.variableName, self.value)

	def run(self,frame,ff):
		return frame.set(self.variableName,self.value)