# -*- coding: utf-8 -*-
from math import floor
from lexer import Lexer

class Frame:

	def __init__(self,parent):
		self.locals =  {}
		self.parent = parent

	def set (self, name, value):
		if hasattr(value, 'literal'): #uloží se jenom literal, zbytek se nejdřív pustí, aby z toho vyšel literal
			self.locals[name] = value
		else:
			self.locals[name] = value.run(self, None)

	def get (self, name):
		if (name in self.locals):
			return self.locals[name]
		if (self.parent == None): #pokud není rodič, nemůžu se podívat nahoru a tím pádem proměná neexistuje
			raise
		return self.parent.get(self.name)

class FunctionFrame:

	def __init__(self):
		self.functions = {}

	def add (self, name, arrgs, block):
		self.functions[name] = [arrgs, block]

	def get (self, name):
		return self.functions[name]


class Block:
	""" Blok prikazu. 

	Nejedna se o nic jineho, nez o seznam prikazu, ktere jdou po sobe. 
	"""

	def __init__(self):
		self.code = []

	def add(self, node):
		""" Prida novy prikaz. """
		self.code.append(node)

	def add_zacatek(self,node):
		""" Přidá nový příkaz na začátek bloku"""
		self.code = [node] + self.code

	def __str__(self):
		self.result = "{"
		for node in self.code:
			self.result = self.result + "\n" + node.__str__()
		self.result = self.result + "\n}\n"
		return self.result

	def run(self, frame,ff):
		for prikaz in self.code:
			if (prikaz.type!="Return"):
				prikaz.run(frame,ff)
			else:
				return prikaz.run(frame,ff)	 

class BinaryOperator:
	""" Binary operator. 

	Pamatuje si levy a pravy operand a typ operace, kterou s nimi ma provest. """
	def __init__(self, left, right, operator):
		self.left = left
		self.right = right
		self.operator = operator
		self.type = "BinaryOperator"
	
	def __str__(self):
		return "( %s %s %s )" % (self.left, self.operator, self.right)

	def run(self, frame,ff):
		l = self.left.run(frame,ff)
		r = self.right.run(frame,ff) 
		le = Lexer() #abychom si mohli číst typy operátorů

		if self.operator == le.OP_OR:
			if l == True or r == True:
				return Literal(True)
			else:
				return Literal(False)

		elif self.operator == le.OP_AND:
			if l == True and r == True:
				return Literal(True)
			else:
				return Literal(False)

		elif self.operator == le.OP_EQUAL:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) == int(r) )
				else:
					return Literal(float(l) == float(r) )
			else:
				return Literal(False)

		elif self.operator == le.OP_NOTEQUAL:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) != int(r) )
				else:
					return Literal(float(l) != float(r) )
			else:
				return Literal(False)

		elif self.operator == le.OP_BIGGER:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) > int(r) )
				else:
					return Literal(float(l) > float(r) )
			else:
				return Literal(False)

		elif self.operator == le.OP_BIGGEROREQUAL:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) > int(r) )
				else:
					return Literal(float(l) >= float(r) )
			else:
				return Literal(False)

		elif self.operator == le.OP_SMALLER:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) < int(r) )
				else:
					return Literal(float(l) < float(r) )
			else:
				return Literal(False)

		elif self.operator == le.OP_SMALLEROREQUAL:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) <= int(r) )
				else:
					return Literal(float(l) <= float(r) )
			else:
				return Literal(False)

		elif self.operator == le.OP_ADD:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) + int(r) )
				else:
					return Literal(float(l) + float(r) )
			else:
				return l + r

		elif self.operator == le.OP_SUBSTRACT:
			if ( self.isfloat(l) and self.isfloat(r) ): #jsou to čísla, vezme to i float
				if ( self.isint(l) and self.isint(r) ): # pouze celá čísla
					return Literal(int(l) - int(r) )
				else:
					return Literal(float(l) - float(r) )
			else:
				raise BaseException("Nemůžeš odečíst dva stringy nebo string s číslem")

		elif self.operator == le.OP_MULTIPLY:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) * int(r) )
				else:
					return Literal(float(l) * float(r) )
			else:
				raise BaseException("Nemůžeš násobit dva stringy nebo string s číslem")

		elif self.operator == le.OP_MOCNIT:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) ** int(r) )
				else:
					return Literal(float(l) ** float(r) )
			else:
				raise BaseException("Nemůžeš mocnit dva stringy nebo string s číslem")

		elif self.operator == le.OP_DIVIDE:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) / int(r) )
				else:
					return Literal(float(l) / float(r) )
			else:
				raise BaseException("Nemůžeš dělit dva stringy nebo string s číslem")

		elif self.operator == le.OP_FLOORDIVISION:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) / int(r) )
				else:
					return Literal(floor( float(l) / float(r) ) )
			else:
				raise BaseException("Nemůžeš dělit dva stringy nebo string s číslem")

		elif self.operator == le.OP_REMAINDER:
			if ( self.isfloat(l) and self.isfloat(r) ):
				if ( self.isint(l) and self.isint(r) ):
					return Literal(int(l) % int(r) )
				else:
					return Literal(floor( float(l) % float(r) ) )
			else:
				raise BaseException("Nemůžeš dělit dva stringy nebo string s číslem")

	def isint(self,x): #vyzkouší jestli to jde převést na int, vrátí True nebo False
		try:
			int(x)
			return True
		except:
			return False

	def isfloat(self,x): #samé s floatem
		try: 
			float(x)
			return True
		except:
			return False





class VariableRead:
	""" Cteni hodnoty ulozene v promenne. """
	def __init__(self, variableName):
		self.variableName = variableName
		self.type = "variableRead"

	def __str__(self):
		return self.variableName

	def run(self,frame,ff):
		return frame.get(self.variableName).run(frame,ff)

class VariableWrite:
	""" Zapis hodnoty do promenne. Krom nazvu promenne si pamatuje i vyraz, kterym se vypocita hodnota. """
	def __init__(self, variableName, value):
		self.variableName = variableName
		self.value = value
		self.type = "variableWrite"

	def __str__(self):
		return "%s = %s" % (self.variableName, self.value)

	def run(self,frame,ff):
		return frame.set(self.variableName,self.value)

class Literal:
	""" Literal (tedy jakakoli konstanta, cislo). """
	def __init__(self, value):
		self.value = value
		self.literal = True
		self.type = "Literal"

	def __str__(self):
		return str(self.value)

	def run(self, frame,ff):
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

	def run(self, frame,ff):
		self.istrue = 0
		if self.condition.run(frame,None).run(frame,None) == True: #condition.run vrací Literal True nbo False
			self.istrue = 1
			self.trueCase.run(frame,None)
		for i in self.elifs:
			if i[0].run(frame,None).frame(frame,None) == True:
				self.istrue = 1
				i[1].run(frame,None)
		if self.istrue==0:
			self.falseCase.run(frame,None)




class While:
	""" Pamatuje si podmínku a blok, který opakuje 
	KW_WHILE '(' E ')' BLOCK
	 """

	def __init__(self, condition, block):
		self.condition = condition
		self.block = block
		self.type = "While"

	def __str__(self):
		return "while (%s) %s" % (self.condition, self.block)

	def run(self, frame,ff):
		while self.condition.run(frame,None) == True:
			self.block.run(frame,None)

class For:
	""" pamatuje si kam se má ukládat jednotlivý prvek seznamu, seznam a block
	KW_FOR ident KW_IN ( ident | FCALL | FIELD) BLOCK
	"""

	def __init__(self, variable, array, block):
		self.variable = variable
		self.array = array
		self.block = block
		self.type = "For"

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
		self.type = "FunctionWrite"

	def __str__(self):
		if (self.arrgs == []):
			return "function = %s () %s" % (self.name, self.block)
		else:
			a = "function = %s (" % (self.name[1],)
			x=1
			for y in self.arrgs:
				if x == 1:
					a += y.__str__()
				else:
					a += ", "+ y.__str__()
				x+=1
			a += ") " + self.block.__str__()
			return a

	def run(self, frame, ff):
		ff.add(self.name, self.arrgs, self.block)

class FunctionCall:
	def __init__(self, name, arrgs):
		self.name = name
		self.arrgs = arrgs
		self.type = "FunctionCall"

	def __str__(self):
		if (self.arrgs == []):
			return " %s ()" % (self.name[1],)
		else:
			a = "%s ("  % (self.name[1],)
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
		(arrrgumenty, block) = ff.get(self.name)
		novyframe=Frame(frame)
		x=0
		for i in arrrgumenty:
			block.add_zacatek(VariableWrite(i.run(frame,ff),self.arrgs[x]))
			#novyframe.set(i.__str__(),Literal(self.arrgs[x].run(frame,ff)))
			x+=1
		return block.run(novyframe,ff)
		print novyframe.locals


class ArrgIdent:
	def __init__(self,name):
		self.name = name
		self.type = "ArrgIdent"

	def __str__(self):
		return self.name

	def run(self, frame, ff):
		return self.name

class Array:
	def __init__(self,polozkypole):
		self.polozkypole = polozkypole
		self.type = "Array"

	def __str__(self):
		a = "["
		for i in self.polozkypole:
			if (a == "["):
				a += i
			else:
				a += "," + i
		a += "]"
		return a

class Print:
	def __init__(self,what):
		self.what = what
		self.type = "Print"

	def __str__(self):
		return "print ( %s )" % (self.what)

	def run(self, frame,ff):
		print self.what.run(frame,None)

class Return:
	def __init__(self,what):
		self.what = what
		self.type = "Return"

	def __str__(self):
		return "return  %s " % (self.what)

	def run(self, frame,ff):
		return self.what.run(frame,None)