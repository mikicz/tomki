# -*- coding: utf-8 -*-
from Frame import Frame
from VariableWrite import VariableWrite
from ReturnThingy import ReturnThingy

class FunctionCall:
	def __init__(self, name, arrgs):
		self.name = name
		self.arrgs = arrgs	# arrgs je seznam hodnot argumentů
		self.type = "FunctionCall"

	def __str__(self):
		if (self.arrgs == []):
			return " %s ()" % (self.name,)
		else:
			a = "%s ("  % (self.name)
			x = 1
			for y in self.arrgs:
				if (x == 1):
					a += str(y.__str__())
				else:
					a += ", "+ str(y.__str__())
				x += 1
			a += ") "
			return a

	def run (self, frame, functionFrame):
		(arrrgumenty, block) = functionFrame.get(self.name.run(frame, functionFrame))
		novyframe = Frame(frame)
		for i in range(0, len(arrrgumenty)):
			novyframe.set(arrrgumenty[i].name, self.arrgs[i], functionFrame)
		try:
			block.run(novyframe, functionFrame)
		except Literal, e:
			return e
		#print novyframe.locals