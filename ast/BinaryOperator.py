# -*- coding: utf-8 -*-
from lexer import Lexer
from Literal import Literal

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
		while(hasattr(l,"type")): #pojistka, když se nějak vrátí Literal nebo něco místo toho, co by mělo (int, str, list)
			l = l.run(frame,ff)
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
			elif (isinstance(l, list) and isinstance(r, list)):
				return l+r
			else:
				return str(l) + str(r)

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
