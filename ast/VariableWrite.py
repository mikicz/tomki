# -*- coding: utf-8 -*-
class VariableWrite:
	""" Zapis hodnoty do promenne. Krom nazvu promenne si pamatuje i vyraz, kterym se vypocita hodnota. """
	def __init__(self, variableName, value, index=None):
		self.variableName = variableName
		self.value = value
		self.type = "variableWrite"
		self.index = index

	def __str__(self):
		if (self.index == None):
			return "%s = %s" % (self.variableName, self.value)
		else:
			return "%s[%s] = %s" % (self.variableName, self.index, self.value)

	def run(self, frame, functionFrame):
		if (self.index == None):
			return frame.set(self.variableName, self.value, functionFrame)
		else:
			array = frame.get(self.variableName).run(frame, functionFrame)
			array[self.index.run(frame,functionFrame)] = self.value
			return frame.set(self.variableName,array,functionFrame)