# -*- coding: utf-8 -*-
class FunctionWrite:
	"""pamatuje si jméno funkce, parametry a blok
	KW_FUNCTION OP_ASSING ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT BLOCK
	"""

	def __init__(self, name, arrgs, block):
		self.name = name 
		self.arrgs = arrgs
		self.block = block
		self.type = "FunctionWrite"

	def __str__(self):
		if (self.arrgs == []):
			return "function %s () %s" % (self.name, self.block)
		else:
			a = "function %s (" % (self.name,)
			x=1
			for y in self.arrgs:
				if x == 1:
					a += y.__str__()
				else:
					a += ", "+ y.__str__()
				x+=1
			a += ") " + self.block.__str__()
			return a

	def run(self, frame, functionFrame):
		functionFrame.add(self.name, self.arrgs, self.block)