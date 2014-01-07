# -*- coding: utf-8 -*-
from math import floor
from lexer import Lexer
class Frame:

	def __init__(self,parent):
		self.locals =  {}
		self.parent

	def set (self, name, value):
		self.locals[name] = value

	def get (self, name):
		if (name in self.locals):
			return self.locals[name]
		if (self.parent == None):
			pass
			#vyhoď error
		return self.parent.get(self.name)

class Block:
	""" Blok prikazu. 

	Nejedna se o nic jineho, nez o seznam prikazu, ktere jdou po sobe. 
	"""

	def __init__(self):
		self.code = []

	def add(self, node):
		""" Prida novy prikaz. """
		self.code.append(node)

	def __str__(self):
		self.result = "{"
		for node in self.code:
			self.result = self.result + "\n" + node.__str__()
		self.result = self.result + "\n}\n"
		return self.result

	def run(self, frame):
		for prikaz in self.code:
			prikaz.run(frame)	 

class BinaryOperator:
	""" Binary operator. 

	Pamatuje si levy a pravy operand a typ operace, kterou s nimi ma provest. """
	def __init__(self, left, right, operator):
		self.left = left
		self.right = right
		self.operator = operator
	
	def __str__(self):
		return "( %s %s %s)" % (self.left, self.operator, self.right)
	def run(self, frame):
		Lex = Lexer()
		l = self.left.run(frame)
		r = self.right.run(frame) #hodil by se check jestli to jsou čísla (pro některý operace to holt bez čísel nejde)

		if self.operator == Lex.OP_OR:
			if l == True or r == True:
				return True
			else:
				return False
		elif self.operator == Lex.OP_AND:
			if l == True and r == True:
				return True
			else:
				return False
		elif self.operator == Lex.OP_EQUAL:
			return l==r
		elif self.operator == Lex.OP_NOTEQUAL:
			return l!=r
		elif self.operator == Lex.OP_BIGGER:
			return l>r
		elif self.operator == Lex.OP_BIGGEROREQUAL:
			return l>=r
		elif self.operator == Lex.OP_SMALLER:
			return l<r
		elif self.operator == Lex.OP_SMALLEROREQUAL:
			return l<=r
		elif self.operator == Lex.OP_ADD:
			return l+r
		elif self.operator == Lex.OP_SUBSTRACT:
			return l-r
		elif self.operator == Lex.OP_MULTIPLY:
			return l*r
		elif self.operator == Lex.OP_MOCNIT:
			return l**r
		elif self.operator == Lex.OP_DIVIDE:
			return l/r
		elif self.operator == Lex.OP_FLOORDIVISION:
			return floor(l/r)
		elif self.operator == Lex.OP_REMAINDER:
			return l%r


class VariableRead:
	""" Cteni hodnoty ulozene v promenne. """
	def __init__(self, variableName):
		self.variableName = variableName

	def __str__(self):
		return self.variableName

	def run(self,frame):
		return frame.get(self.name)

class VariableWrite:
	""" Zapis hodnoty do promenne. Krom nazvu promenne si pamatuje i vyraz, kterym se vypocita hodnota. """
	def __init__(self, variableName, value):
		self.variableName = variableName
		self.value = value

	def __str__(self):
		return "%s = %s" % (self.variableName, self.value)

	def run(self,frame):
		return frame.set(self.variableName,self.value.run(frame))

class Literal:
	""" Literal (tedy jakakoli konstanta, cislo). """
	def __init__(self, value):
		self.value = str(value)

	def __str__(self):
		return self.value

	def run(self, frame):
		return self.value

class If:
	""" Prikaz if. Pamatuje si vyraz ktery je podminkou a pak bloky pro true a else casti. 

	CONDITION ::= KW_IF '(' E ')' BLOCK { KW_ELIF '(' E ')' BLOCK } [ KW_ELSE BLOCK ]

	"""
	def __init__(self, condition, trueCase, elifs, falseCase):
		self.condition = condition
		self.trueCase = trueCase
		self.elifs = elifs # prázdné [], ve formátu [[condition, block], ...]
		self.falseCase = falseCase

	def __str__(self):
		if self.elifs == []:
			a = "if (%s) %s else %s" % (self.condition, self.trueCase, self.falseCase)
		else:
			a = "if ("+self.condition+") " + self.trueCase
			for x in self.elifs:
				a += " elif ("+x[0]+") " + x[1]
			a+= " else " + self.falseCase
		return a
	def run(self, frame):
		self.istrue = 0
		if self.condition.run(frame) == True:
			self.istrue = 1
			self.trueCase.run(frame)
		for i in self.elifs:
			if i[0] == True:
				self.istrue = 1
				i[1].run(frame)
		if self.istrue==0:
			self.falseCase.run(frame)




class While:
	""" Pamatuje si podmínku a blok, který opakuje 
	KW_WHILE '(' E ')' BLOCK
	 """

	def __init__(self, condition, block):
		self.condition = condition
		self.block = block

	def __str__(self):
		return "while (%s) %s" % (self.condition, self.block)
	def run(self, frame):
		while self.condition.run == True:
			self.block.run(frame)

class For:
	""" pamatuje si kam se má ukládat jednotlivý prvek seznamu, seznam a block
	KW_FOR ident KW_IN ( ident | FCALL | FIELD) BLOCK
	"""

	def __init__(self, variable, array, block):
		self.variable = variable
		self.array = array
		self.block = block

	def __str__(self):
		return "for (%s) in %s %s" % (self.variable, self.array, self.block)

class FunctionWrite:
	"""pamatuje si jméno funkce, parametry a blok
	KW_FUNCTION OP_ASSING ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT BLOCK
	"""

	def __init__(self, name, arrgs, block):
		self.name = name
		self.arrgs = arrgs
		self.block = block

	def __str__(self):
		if (self.arrgs == []):
			return "function = %s () %s" % (self.name, self.block)
		else:
			a = "function = %s ("
			x=1
			for y in self.arrgs:
				if x == 1:
					a += y
				else:
					a += ", "+ y
			a += ") " + self.block
			return a

class FunctionCall:
	def __init__(self, name, arrgs):
		self.name = name
		self.arrgs = arrgs
		self.block = block

	def __str__(self):
		if (self.arrgs == []):
			return " %s () %s" % (self.name, self.block)
		else:
			a = "%s ("
			x=1
			for y in self.arrgs:
				if x == 1:
					a += y
				else:
					a += ", "+ y
			a += ") "
			return a

class ArrgIdent:
	def __init__(self,name):
		self.name = name

	def __str__(self):
		return self.name

class Array:
	def __init__(self,polozkypole):
		self.polozkypole = polozkypole

	def __str__(self):
		a = "["
		for i in self.polozkypole:
			if (a == "["):
				a += i
			else:
				a += "," + i
		a += "]"
		return a





