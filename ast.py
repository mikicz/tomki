# -*- coding: utf-8 -*-
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
		result = "{"
		for node in self.code:
			result = result + "\n" + node.__str__()
		result = result + "\n}\n"
		return result		 

class BinaryOperator:
	""" Binary operator. 

	Pamatuje si levy a pravy operand a typ operace, kterou s nimi ma provest. """
	def __init__(self, left, right, operator):
		self.left = left
		self.right = right
		self.operator = operator
	
	def __str__(self):
		return "( %s %s %s)" % (self.left, self.operator, self.right)

class VariableRead:
	""" Cteni hodnoty ulozene v promenne. """
	def __init__(self, variableName):
		self.variableName = variableName

	def __str__(self):
		return self.variableName

class VariableWrite:
	""" Zapis hodnoty do promenne. Krom nazvu promenne si pamatuje i vyraz, kterym se vypocita hodnota. """
	def __init__(self, variableName, value):
		self.variableName = variableName
		self.value = value

	def __str__(self):
		return "%s = %s" % (self.variableName, self.value)

class Literal:
	""" Literal (tedy jakakoli konstanta, cislo). """
	def __init__(self, value):
		self.value = str(value)

	def __str__(self):
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


class While:
	""" Pamatuje si podmínku a blok, který opakuje 
	KW_WHILE '(' E ')' BLOCK
	 """

	def __init__(self, condition, block):
		self.condition = condition
		self.block = block

	def __str__(self):
		return "while (%s) %s" % (self.condition, self.block)

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

class Function:
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





