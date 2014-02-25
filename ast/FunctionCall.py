# -*- coding: utf-8 -*-
from Frame import Frame
from VariableWrite import VariableWrite

class FunctionCall:
	def __init__(self, name, arrgs):
		self.name = name
		self.arrgs = arrgs
		self.type = "FunctionCall"

	def __str__(self):
		if (self.arrgs == []):
			return " %s ()" % (self.name,)
		else:
			a = "%s ("  % (self.name,)
			x=1
			for y in self.arrgs:
				if x == 1:
					a += y.__str__()
				else:
					a += ", "+ y.__str__()
				x+=1
			a += ") "
			return a

	def run (self, frame, ff):
		(arrrgumenty, block) = ff.get(self.name.run(frame, ff))
		novyframe=Frame(frame)
		x=0
		for i in arrrgumenty:
			block.add_zacatek(VariableWrite(i.run(frame,ff),self.arrgs[x]))
			#novyframe.set(i.__str__(),Literal(self.arrgs[x].run(frame,ff)))
			x+=1
		return block.run(novyframe,ff)
		print novyframe.locals