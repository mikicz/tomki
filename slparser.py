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

	def top(self):
		""" Abych nemusel tolik psat, provede top() z lexeru. 
		"""
		return self.lexer.topToken()

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
		""" EXPRESSION ::= E2 { op_eq E2 }
	   
		Porovnani ma nejnizsi prioritu, a je binarni operator.
	    """
		lhs = self.parseE2()
		while (self.top()[0] == Lexer.OP_EQ):
			self.pop()
			rhs = self.parseE2()
			lhs = BinaryOperator(lhs, rhs, Lexer.OP_EQ)
		return lhs

	def parseE2(self):
		""" E2 ::= F { op_add | op_sub F }
	   
		Druhy level priorit je scitani a odcitani. Opet se jedna o binarni operatory. 
	    """
		lhs = self.parseF()
		while (self.top()[0] in (Lexer.OP_ADD, Lexer.OP_SUB)):
			op = self.pop()[0]
			rhs = self.parseE2()
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
		""" IF_STATEMENT ::= if op_paropen EXPRESSION op_parclose [ BLOCK ] [ else BLOCK ]
	   
	    If podminka je klasicky podminka a za ni if, pripadne else block. Vsimnete si, ze oba dva jsou vlastne v moji gramatice nepovinne. 
	    """
		self.pop(Lexer.KW_IF)
		self.pop(Lexer.OP_PAROPEN)
		condition = self.parseExpression()
		self.pop(Lexer.OP_PARCLOSE)
		trueCase = Block() # to aby se nam chybeji vetev sprave zobrazila jako {}
		falseCase = Block() # to aby se nam chybeji vetev sprave zobrazila jako {}
		if (self.top()[0] == Lexer.OP_BRACEOPEN): # kdyz hned po podmince je {, vim ze je to if cast
			trueCase = self.parseBlock()
		if (self.top()[0] == Lexer.KW_ELSE): # jinak za ifem muze byt jeste else pro else cast
			self.pop()
			falseCase = self.parseBlock()
		# cokoli ostatniho by bylo za ifem, neni soucasti ifu
		return If(condition, trueCase, falseCase)

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
