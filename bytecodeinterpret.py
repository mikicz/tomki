# -*- coding: utf-8 -*-

class BytecodeInterpret:
	def __init__(self):
		self.code = []
		self.variables = {} #tady budou jenom jednoduché proměnné
		self.tempvariables = 0
		self.arrays = [] #tady budou jenom pole
		self.commands = {"load":0, # load t1 1
						 "copy":1,  # load t2 t1

						 #binary operators
						 "add":2, # add res op1 op2
						 "sub":3, 
						 "mul":4,
						 "div":5,
						 "exp":6, #mocnění
						 "floordiv":7, #floordivision
						 "rem":8, #remainder
						 "or":20, 
						 "and":21,
						 "eq":22,
						 "neq":23,
						 "big":25,
						 "bigoreq":24,
						 "sma":26,
						 "smaoreq":27,

						 #prace s polemi
						 "array":9, #array name
						 "append":10, #append name what
						 "insert":11, #insert name what where
						 "join":12, #join res what1 what2
						 "len":13, #len res ofwhat
						 "pop":14, #pop res array index
						 "loadfromarray":15, #loadfromarray res array index

						 #funkce
						 "return":16, #return op

						 #jumps
						 "jump":17, #jump where
						 "ifelse":18, #iffalse what where
						 "ifelif":19, #ifelif what
						 "addr":28 #vytoření adresy 




		}

	def tempvariable(self):
		self.tempvariables+=1
		return "t"+str(self.tempvariables)

	def addinstruction(self,typ,par1,par2=None,par3=None):
		if (par2==None and par3==None):
			self.code.append([typ,par1])
		elif (par3==None):
			self.code.append([typ,par1,par2])
		else:
			self.code.append([typ,par1,par2,par3])

		if (typ == "load" or "copy"):
			self.variables[par1]=len(self.variables)-1


	def __str__(self):
		a = ""
		for i in self.code:
			a += str(i) + "\n"
		return a