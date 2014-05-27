# -*- coding: utf-8 -*-
class VariableRead:
	""" Cteni hodnoty ulozene v promenne. """
	def __init__(self, variableName, index=None):
		self.variableName = variableName
		self.index = index
		self.type = "variableRead"

	def __str__(self):
		if self.index == None:
			return self.variableName
		else:
			return str(self.variableName)+"["+str(self.index)+"]"

	def run(self,frame, functionFrame):
		if self.index == None:
			return frame.get(self.variableName)
		else:
			array = frame.get(self.variableName).run(frame,functionFrame)
			if (self.index.type != "Literal"):
				self.index = self.index.run(frame,functionFrame)
			x = array[self.index.run(frame,functionFrame)]
			return x

	def compile(self,block):
		res = block.tempvariable()
		block.addinstruction("copy",res,self.variableName)
		return res