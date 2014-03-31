# -*- coding: utf-8 -*-
class VariableRead:
	""" Cteni hodnoty ulozene v promenne. """
	def __init__(self, variableName, index=None):
		self.variableName = variableName
		self.index = index
		self.type = "variableRead"

	def __str__(self):
		return self.variableName

	def run(self,frame, functionFrame):
		return frame.get(self.variableName).run(frame, functionFrame, self.index)

	def compile(self,block):
		res = block.tempvariable()
		block.addinstruction("copy",res,self.variableName)
		return res