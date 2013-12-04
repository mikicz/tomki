# -*- coding: utf-8 -*-
from ast import *
from lexer import Lexer

class Parser:
	""" Jednoduchy priklad parseru. Naparsuje nasledujici gramatiku:

	PROGRAM ::= { STATEMENT }
	STATEMENT ::= IF_STATEMENT | ASSIGNMENT
	ASSIGNMENT ::= ident op_assign EXPRESSION
	EXPRESSION ::= E2 { op_eq E2 }
	E2 ::= F { op_add | op_sub F }
	F ::= number | ident | op_paropen EXPRESSION op_parclose
	IF_STATEMENT ::= if op_paropen EXPRESSION op_parclose [ BLOCK ] [ else BLOCK ]
	BLOCK ::= op_braceopen { STATEMENT } op_braceclose

	Ten parser se trosku lisi od toho parseru, ktery jsme delali na hodine, protoze uz pouziva ty jednoduzsi stromy, o kterych jsem mluvil. Takze misto toho, aby kazde pravidlo melo svoji vlasti tridu (v ast), tak ty tridy pro ten strom odpovidaji spis tomu, co ten program bude delat, nez tomu, jak je napsana gramatika. Blizsi popisky viz jednotlive parsovaci metody nize.
	"""


	def __init__(self, lexer):
		""" Zalozi parser a zapamatuje si lexer, se kterym bude pracovat. """
		self.lexer = lexer
		pass


	def pop(self, type = None):
		""" Abych nemusel tolik psat, provede pop z lexeru. Kdyz specifikuju druh tokenu, ktery ocekavam, tak zaroven zkontroluje jestli je to spravny typ, a vyhodi vyjimku, kdyz tomu tak neni. 
		"""
		if (type is None):
			return self.lexer.popToken()
		t = self.lexer.topToken()
		if (t[0] == type):
			return self.lexer.popToken()
		else:
			raise SyntaxError("Ocekavany token " + type + " neni na vstupu (" + t[0] + " misto nej)")

	def top(self, i = 0):
		""" Abych nemusel tolik psat, provede top() z lexeru. 
		"""
		return self.lexer.topToken(i)

	def parse(self):
		""" Hlavni metoda na parsovani, odpovida pravidlu pro program:

		PROGRAM ::= { STATEMENT }

		Z hlediska stromu (ast) je program tedy blok prikazu, postupne jak prikazy parsuju tak je pridavam do toho bloku. Kdyz zjistim, ze uz na vstupu zadny token nemam, tak jsem skoncil.
		"""
		program = Block()
		while (self.top()[0] != Lexer.EOF):
			program.add(self.parseStatement())
		return program

	def parseStatement(self):
		""" STATEMENT ::= ( CONDITION | LOOP | E | FDEF ) ;

		Statement je bud if, nebo zapis promenne. 
		"""
		if (self.top()[0] == Lexer.KW_IF): #podmínka
			return self.parseIfStatement()
		elif (self.top()[0] == Lexer.KW_WHILE): #while
			return self.parseWhile()
		elif (self.top()[0] == Lexer.KW_FOR): #for
			return self.parseFor()
		elif (self.top()[0] == Lexer.KW_FUNCTION): #funkce
			return self.parseFunction
		else:
			return self.parseAssignment()

	def parseAssignment(self):
		""" ASSIGNMENT ::= ident op_assign EXPRESSION
	   
		Ulozeni hodnoty do promenne vypada tak, ze na leve strane je identifikator promenne, hned za nim je operator prirazeni a za nim je vyraz, ktery vypocitava hodnotu, kterou do promenne chci ulozit. Tohle je zjednodusena verze prirazeni, viz komentare k hodine. 
		"""
		variableName = self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.OP_ASSIGN)
		rhs = self.parseExpression()
		return VariableWrite(variableName, rhs)

	def parseExpression(self):
		""" EXPRESSION ::= E1 [ OP_ASSIGN E1 ]
	   
		"""
		lhs = self.parseE1()
		while (self.top()[0] == Lexer.OP_ASSIGN):
			self.pop()
			rhs = self.parseE1()
			lhs = BinaryOperator(lhs, rhs, Lexer.OP_ASSIGN)
		return lhs

	def parseE1(self):
		""" E1 ::= E2 { OP_OR E2 }
		"""
		lhs = self.parseE2()
		while (self.top()[0] == Lexer.OP_OR):
			self.pop()[0]
			rhs = self.parseE2()
			lhs = BinaryOperator(lhs, rhs, Lexer.OP_OR)
		return lhs

	def parseE2(self):
		""" E2 ::= E3 { OP_OR E3 }
		"""
		lhs = self.parseE3()
		while (self.top()[0] == Lexer.OP_AND):
			self.pop()[0]
			rhs = self.parseE3()
			lhs = BinaryOperator(lhs, rhs, Lexer.OP_AND)
		return lhs

	def parseE3(self):
		""" E3 ::= E4 { ( OP_EQUAL | OP_NOTEQUAL ) E4 }
	
		Druhy level priorit je scitani a odcitani. Opet se jedna o binarni operatory. 
		"""
		lhs = self.parseE4()
		while (self.top()[0] in (Lexer.OP_EQUAL, Lexer.OP_NOTEQUAL)):
			op = self.pop()[0]
			rhs = self.parseE4()
			lhs = BinaryOperator(lhs, rhs, op)
		return lhs
	
	def parseE4(self):
		""" E4 ::= E5 { ( OP_BIGGER | OP_SMALLER | OP_BIGGEROREQUAL | OP_SMALLEROREQUAL ) E5 }
	
		Druhy level priorit je scitani a odcitani. Opet se jedna o binarni operatory. 
		"""
		lhs = self.parseE4()
		while (self.top()[0] in (Lexer.OP_EQUAL, Lexer.OP_NOTEQUAL)):
			op = self.pop()[0]
			rhs = self.parseE4()
			lhs = BinaryOperator(lhs, rhs, op)
		return lhs

	def parseF(self):
		""" F ::= number | ident | op_paropen EXPRESSION op_parclose
		
		Faktorem vyrazu pak je bud cislo (literal), nebo nazev promenne, v tomto pripade se vzdycky jedna o cteni promenne a nebo znova cely vyraz v zavorkach. 
		"""
		if (self.top()[0] == Lexer.NUMBER):
			value = self.pop()[1]
			return Literal(value)
		elif (self.top()[0] == Lexer.IDENT):
			variableName = self.pop()[1]
			return VariableRead(variableName)
		else:
			self.pop(Lexer.OP_PAROPEN)
			result = self.parseExpression()
			self.pop(Lexer.OP_PARCLOSE)
			return result 

	def parseIfStatement(self):
		""" 
		CONDITION ::= KW_IF '(' E ')' BLOCK { KW_ELIF '(' E ')' BLOCK } [ KW_ELSE BLOCK ]
	
		If podminka je klasicky podminka a za ni if, pripadne else block.
		"""
		self.pop(Lexer.KW_IF)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		condition = self.parseExpression()
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		trueCase = self.parseBlock()

		elifs = []
		while (self.top[0] == Lexer.KW_ELIF):
			self.pop()
			self.pop(Lexer.OP_PARENTHESES_LEFT)
			x = self.parseExpression() #podmínka 
			self.pop(Lexer.OP_PARENTHESES_RIGHT)
			y = self.parseBlock() #blok
			elifs.append([x,y])

		if (self.top()[0] == Lexer.KW_ELSE): # za elify muze byt ještě else
			self.pop()
			falseCase = self.parseBlock()
		else: # to aby se nam chybeji vetev sprave zobrazila jako {}
			falseCase = Block() 
		
		# cokoli ostatniho by bylo za ifem, neni soucasti ifu
		return If(condition, trueCase,elifs, falseCase)

	def parseWhile(self):
		"""
		KW_WHILE '(' E ')' BLOCK
		"""

		self.pop(Lexer.KW_WHILE)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		condition = self.parseExpression()
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		block = self.parseBlock()

		return While(condition, block)

	def parseFor(self):
		"""
		KW_FOR ident KW_IN ( ident | FCALL | FIELD) BLOCK
		"""

		self.pop(Lexer.KW_FOR)
		var = self. # ident
		self.pop(Lexer.KW_In)
		if ( self.top()[0] == Lexer.IDENT and self.top(1)[0] == Lexer.OP_PARENTHESES_LEFT ):
			array = self. #function call
		elif ( self.top()[0] == Lexer.IDENT ):
			array = self. # ident
		elif ( self.top()[0] == Lexer.OP_BRACKETS_LEFT ):
			array = self. # pole
		block = self.parseBlock()
		return For(var,array,block)

	def parseBlock(self):
		""" BLOCK ::= op_braceopen { STATEMENT } op_braceclose

		Blok je podobny programu, proste nekolik prikazu za sebou. 
		"""
		self.pop(Lexer.OP_BRACEOPEN)
		result = Block()
		while (self.top()[0] != Lexer.OP_BRACECLOSE):
			result.add(self.parseStatement())
		self.pop(Lexer.OP_BRACECLOSE)
		return result
