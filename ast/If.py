# -*- coding: utf-8 -*-
class If:
	""" Prikaz if. Pamatuje si vyraz ktery je podminkou a pak bloky pro true a else casti. 

	CONDITION ::= KW_IF '(' E ')' BLOCK { KW_ELIF '(' E ')' BLOCK } [ KW_ELSE BLOCK ]

	"""
	def __init__(self, condition, trueCase, elifs, falseCase):
		self.condition = condition
		self.trueCase = trueCase
		self.elifs = elifs # prázdné [], ve formátu [[condition, block], ...]
		self.falseCase = falseCase
		self.type = "If"

	def __str__(self):
		if self.elifs == []:
			a = "if (%s) %s else %s" % (self.condition, self.trueCase, self.falseCase)
		else:
			a = "if ( %s ) %s \n" % (self.condition, self.trueCase)
			for x in self.elifs:
				a += "elif ( %s ) %s \n" % (x[0], x[1])
			a+= "else %s " % (self.falseCase)
		return a

	def run(self, frame, functionFrame):
		self.istrue = 0
		if self.condition.run(frame, functionFrame).run(frame, functionFrame) == True: #condition.run vrací Literal True nbo False
			self.istrue = 1
			self.trueCase.run(frame, functionFrame)
		for i in self.elifs:
			if i[0].run(frame, functionFrame).frame(frame,None) == True:
				self.istrue = 1
				i[1].run(frame, functionFrame)
		if self.istrue==0:
			for i in self.elifs:
				if (self.istrue == 0):
					if i[0].run(frame, functionFrame).frame(frame,None) == True:
						self.istrue = 1
						i[1].run(frame, functionFrame)
			if (self.istrue == 0):
				self.falseCase.run(frame, functionFrame)

	def compile(self,block):
		if (len(self.elifs)==0):
			res = self.condition.compile(block)
			block.addinstruction("ifelse",res,"falseCase")
			self.trueCase.compile(block)
			block.addinstruction("jump", "end")
			block.addinstruction("addr","falseCase")
			self.falseCase.compile(block)
			block.addinstruction("addr", "end")
		else:
			res = self.condition.compile(block)
			block.addinstruction("ifelif",res)
			self.trueCase.compile(block)
			block.addinstruction("jump", "end")
			x = 1
			l = len(self.elifs)
			for i in self.elifs:
				if (x != l):
					block.addinstruction("addr","elif")
					res = i[0].compile(block)
					block.addinstruction("ifelif",res)
					i[1].compile(block)
					block.addinstruction("jump", "end")
					x += 1
				else:
					block.addinstruction("addr","elif")
					res = i[0].compile(block)
					block.addinstruction("ifelse",res,"falseCase")
					i[1].compile(block)
					block.addinstruction("jump", "end")
			block.addinstruction("addr","falseCase")
			self.falseCase.compile(block)
			block.addinstruction("addr","end")
			
			block.addinstruction("addr","falseCase")
			self.falseCase.compile(block)
			block.addinstruction("addr", "end")
