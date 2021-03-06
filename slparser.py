# -*- coding: utf-8 -*-
from ast import *
from lexer import Lexer
import sys
sys.path.append('ast/')
from ast import *

class Parser:
	"""
	Ten parser se trosku lisi od toho parseru, ktery jsme delali na hodine, protoze uz pouziva ty jednoduzsi stromy, o kterych jsem mluvil. Takze misto toho, aby kazde pravidlo melo svoji vlasti tridu (v ast), tak ty tridy pro ten strom odpovidaji spis tomu, co ten program bude delat, nez tomu, jak je napsana gramatika. Blizsi popisky viz jednotlive parsovaci metody nize.
	"""


	def __init__(self, lexer):
		""" Zalozi parser a zapamatuje si lexer, se kterym bude pracovat. """
		self.lexer = lexer


	def pop(self, type = None):
		""" Abych nemusel tolik psat, provede pop z lexeru. Kdyz specifikuju druh tokenu, ktery ocekavam, tak zaroven zkontroluje jestli je to spravny typ, a vyhodi vyjimku, kdyz tomu tak neni. 
		"""
		if (type is None):
			return self.lexer.popToken()
		t = self.lexer.topToken()
		if (t[0] == type):
			return self.lexer.popToken()
		else:
			raise SyntaxError("Ocekavany token " + type + " neni na vstupu " + str(t[0]) + " misto nej na radku " + str(t[2])+".")

	def top(self, i = 0):
		""" Abych nemusel tolik psat, provede top() z lexeru. 
		Může se zeptat na token + i
		"""
		return self.lexer.topToken(i)

	def parse(self):
		""" Hlavni metoda na parsovani, odpovida pravidlu pro program:

		PROGRAM ::= { STATEMENT }

		Z hlediska stromu (ast) je program tedy blok prikazu, postupne jak prikazy parsuju tak je pridavam do toho bloku. Kdyz zjistim, ze uz na vstupu zadny token nemam, tak jsem skoncil.
		"""
		program = Block()
		while (self.top()[0] != Lexer._EOF):
			program.add(self.parseStatement())
			self.pop()
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
			return self.parseFunction()

		elif (self.top()[0] == Lexer.KW_APPEND): #append
			return self.parseAppend()
		elif (self.top()[0] == Lexer.KW_INSERT): #insert
			return self.parseInsert()
		elif (self.top()[0] == Lexer.KW_LEN): #insert
			return self.parseLen()

		elif (self.top()[0] == Lexer.KW_JOIN): #join
			return self.parseJoin()

		elif (self.top()[0] == Lexer.OP_BRACES_LEFT):
			return self.parseBlock()
		elif (self.top()[0] == Lexer.KW_PRINT):
			return self.parsePrint()
		elif (self.top()[0] == Lexer.KW_RETURN):
			return self.parseReturn()
		elif (self.top()[0] == Lexer.KW_POP):
			return self.parsePop()
		elif (self.top()[0] == Lexer.KW_LEN):
			return self.parseLen()
		elif (self.top(1)[0] == Lexer.OP_PARENTHESES_LEFT):
			return self.parseFunctionCall()
		else:
			return self.parseAssignment()

	def parseAssignment(self):
		""" ASSIGNMENT ::= ident op_assign EXPRESSION
	   
		Ulozeni hodnoty do promenne vypada tak, ze na leve strane je identifikator promenne, hned za nim je operator prirazeni a za nim je vyraz, ktery vypocitava hodnotu, kterou do promenne chci ulozit. Tohle je zjednodusena verze prirazeni, viz komentare k hodine. 
		"""
		
		if (self.top(1)[0] == Lexer.OP_BRACKETS_LEFT):
			variableName = self.pop(Lexer.IDENT)[1]
			self.pop(Lexer.OP_BRACKETS_LEFT)
			index = self.parseExpression()
			self.pop(Lexer.OP_BRACKETS_RIGHT)
			self.pop(Lexer.OP_ASSIGN)
			rhs = self.parseExpression()
			return VariableWrite(variableName, rhs, index=index)
		else:
			variableName = self.pop(Lexer.IDENT)[1]
			self.pop(Lexer.OP_ASSIGN)
			rhs = self.parseExpression()
			return VariableWrite(variableName, rhs)

	def parseExpression(self):
		""" E0 ::= E1 { OP_OR E1 } """
		lhs = self.parseE1()
		while (self.top()[0] == Lexer.OP_OR):
			self.pop()[0]
			rhs = self.parseE1()
			lhs = BinaryOperator(lhs, rhs, Lexer.OP_OR)
		return lhs		

	def parseE1(self):
		""" E1 ::= E2 { OP_AND E2 } """
		lhs = self.parseE2()
		while (self.top()[0] == Lexer.OP_AND):
			self.pop()[0]
			rhs = self.parseE2()
			lhs = BinaryOperator(lhs, rhs, Lexer.OP_AND)
		return lhs

	def parseE2(self):
		""" E2 ::= E3 { ( OP_EQUAL | OP_NOTEQUAL ) E3 } """
		lhs = self.parseE3()
		while (self.top()[0] in (Lexer.OP_EQUAL, Lexer.OP_NOTEQUAL)):
			op = self.pop()[0]
			rhs = self.parseE3()
			lhs = BinaryOperator(lhs, rhs, op)
		return lhs
	
	def parseE3(self):
		""" E3 ::= E4 { ( OP_BIGGER | OP_SMALLER | OP_BIGGEROREQUAL | OP_SMALLEROREQUAL ) E4 } """
		lhs = self.parseE4()
		while (self.top()[0] in (Lexer.OP_BIGGER, Lexer.OP_SMALLER, Lexer.OP_BIGGEROREQUAL, Lexer.OP_SMALLEROREQUAL)):
			op = self.pop()[0]
			rhs = self.parseE4()
			lhs = BinaryOperator(lhs, rhs, op)
		return lhs

	def parseE4(self):
		""" E4 ::= E5 { ( OP_ADD | OP_SUBSTRACT ) E5 } """
		lhs = self.parseE5()
		while (self.top()[0] in (Lexer.OP_ADD, Lexer.OP_SUBSTRACT)):
			op = self.pop()[0]
			rhs = self.parseE5()
			lhs = BinaryOperator(lhs, rhs, op)
		return lhs

	def parseE5(self):
		""" E5 ::= E6 { ( OP_MULTIPLY | OP_MOCNIT | OP_DIVIDE | OP_FLOORDIVISION | OP_REMAINDER ) E6 } """
		lhs = self.parseE6()
		while (self.top()[0] in (Lexer.OP_MULTIPLY, Lexer.OP_MOCNIT, Lexer.OP_DIVIDE, Lexer.OP_FLOORDIVISION, Lexer.OP_REMAINDER)):
			op = self.pop()[0]
			rhs = self.parseE6()
			lhs = BinaryOperator(lhs, rhs, op)
		return lhs

	def parseE6(self):
		""" E6 ::= [ OP_SUBSTRACT ] F """
		if (self.top()[0] == Lexer.OP_SUBSTRACT):
			self.pop(Lexer.OP_SUBSTRACT)[0]
			rhs = self.parseF()
			lhs = BinaryOperator(Literal(0), rhs, Lexer.OP_SUBSTRACT)
		else:
			lhs = self.parseF()
		return lhs

	def parseF(self):
		""" F ::= number | ident [ OP_BRACKETS_LEFT E OP_BRACKETS_RIGHT ] | FCALL | OP_PARENTHESES_LEFT E OP_PARENTHESES_RIGHT| FIELD | STRING
		
		Faktorem vyrazu pak je bud cislo (literal), nebo nazev promenne, v tomto pripade se vzdycky jedna o cteni promenne a nebo znova cely vyraz v zavorkach. 
		"""
		if (self.top()[0] == Lexer.NUMBER):
			value = self.pop()[1]
			return Literal(value)

		elif (self.top()[0] == Lexer.STRING):
			value = self.pop()[1]
			return Literal(value)
		
		elif (self.top()[0] == Lexer.KW_POP): 
			return self.parsePop()

		elif (self.top()[0] == Lexer.KW_LEN): 
			return self.parseLen()

		elif (self.top()[0] == Lexer.KW_JOIN):
			return self.parseJoin()

		elif (self.top()[0] == Lexer.IDENT) and (self.top(1)[0] == Lexer.OP_PARENTHESES_LEFT):
			return self.parseFunctionCall()

		elif (self.top()[0] == Lexer.IDENT) and (self.top(1)[0] != Lexer.OP_BRACKETS_LEFT):
			variableName = self.pop()[1]
			return VariableRead(variableName)

		elif (self.top()[0] == Lexer.IDENT) and (self.top(1)[0] == Lexer.OP_BRACKETS_LEFT): #Čtení hodnoty v seznamu
			variableName = self.pop()[1]
			self.pop(Lexer.OP_BRACKETS_LEFT)
			indexValue = self.parseExpression()
			self.pop(Lexer.OP_BRACKETS_RIGHT)
			return VariableRead(variableName, indexValue)

		

		elif (self.top()[0] == Lexer.OP_BRACKETS_LEFT):
			return self.parseArray()


		else:
			self.pop(Lexer.OP_PARENTHESES_LEFT)
			result = self.parseExpression()
			self.pop(Lexer.OP_PARENTHESES_RIGHT)
			return result 

	def parseIfStatement(self):
		""" 
		CONDITION ::= KW_IF '(' E ')' BLOCK { KW_ELIF '(' E ')' BLOCK } [ KW_ELSE BLOCK ]
	
		If podminka je klasicky podminka a za ni block, nekonečný počet elifů, pak pripadne else block.
		"""
		self.pop(Lexer.KW_IF)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		condition = self.parseExpression()
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		trueCase = self.parseBlock()

		elifs = []
		while (self.top()[0] == Lexer.KW_ELIF):
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
		var = self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.KW_IN)
		if ( self.top()[0] == Lexer.IDENT and self.top(1)[0] == Lexer.OP_PARENTHESES_LEFT ):
			array = self.parseFunctionCall() #function call
		elif ( self.top()[0] == Lexer.IDENT ):
			array = VariableRead(self.pop(Lexer.IDENT)[1])
		elif ( self.top()[0] == Lexer.OP_BRACKETS_LEFT ):
			array = self.parseArray()
		block = self.parseBlock()
		return For(var,array,block)

	def parseBlock(self):
		""" BLOCK ::= op_braceopen { STATEMENT } op_braceclose

		Blok je podobny programu, proste nekolik prikazu za sebou. 
		"""
		self.pop(Lexer.OP_BRACES_LEFT)
		result = Block()
		while (self.top()[0] != Lexer.OP_BRACES_RIGHT):
			result.add(self.parseStatement())
			if self.top()[0] == Lexer.OP_SEMICOLON:
				self.pop(Lexer.OP_SEMICOLON)
		self.pop(Lexer.OP_BRACES_RIGHT)
		return result

	def parseFunctionCall(self):
		""" FCALL ::= ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT """
		functionName=self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		arrgs=[]
		while(self.top()[0] != Lexer.OP_PARENTHESES_RIGHT): 
			arrgs.append(self.parseExpression())
			if self.top()[0] == Lexer.OP_COMMA:
				self.pop(Lexer.OP_COMMA)
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		return FunctionCall(functionName,arrgs)

	def parseFunction(self):
		""" FDEF :== KW_FUNCTION ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT BLOCK """
		self.pop(Lexer.KW_FUNCTION)
		functionName=self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		arrgs=[]
		while(self.top()[0] == Lexer.IDENT): 
			arrgs.append(self.pop(Lexer.IDENT)[1])
			if self.top()[0] == Lexer.OP_COMMA:
				self.pop(Lexer.OP_COMMA)

		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		block = self.parseBlock()
		return FunctionWrite(functionName, arrgs, block)

	def parseArray(self):
		self.pop(Lexer.OP_BRACKETS_LEFT)
		polozkypole = []
		while(self.top()[0] != Lexer.OP_BRACKETS_RIGHT):
			polozkypole.append(self.parseExpression())
			if self.top()[0] == Lexer.OP_COMMA:
				self.pop(Lexer.OP_COMMA)
		self.pop(Lexer.OP_BRACKETS_RIGHT)  #For every upvote this gets I will stroke me penis once. Let's wear the skin off! 
		return Literal(polozkypole)

	def parseAppend(self):
		""" APPEND :== KW_APPEND OP_PARENTHESES_LEFT ident OP_COMMA E OP_PARENTHESES_RIGHT """
		self.pop(Lexer.KW_APPEND)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		array = self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.OP_COMMA)
		value = self.parseExpression()
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		return Append(array, value)

	def parseInsert(self):
		""" INSERT :== KW_INSERT OP_PARENTHESES_LEFT ident OP_COMMA E OP_COMMA E OP_PARENTHESES """
		self.pop(Lexer.KW_INSERT)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		array = self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.OP_COMMA)
		value = self.parseExpression()
		self.pop(Lexer.OP_COMMA)
		index = self.parseExpression()
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		return Insert(array, value, index)

	def parsePop(self):
		""" POP :== KW_POP OP_PARENTHESES_LEFT ident OP_COMMA E OP_PARENTHESES_RIGHT """
		self.pop(Lexer.KW_POP)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		array = self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.OP_COMMA)
		index = self.parseExpression()
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		return Pop(array, index)

	def parseLen(self):
		self.pop(Lexer.KW_LEN)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		ident = self.pop(Lexer.IDENT)[1]
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		return Len(ident)


	def parsePrint(self):
		self.pop(Lexer.KW_PRINT)
		if (self.top()[0] == Lexer.OP_PARENTHESES_LEFT):
			self.pop(Lexer.OP_PARENTHESES_LEFT)
			x = self.parseExpression()
			self.pop(Lexer.OP_PARENTHESES_RIGHT)
		else:
			x = self.parseExpression()
		return Print(x)

	def parseReturn(self):
		self.pop(Lexer.KW_RETURN)
		return Return(self.parseExpression())

	def parseJoin(self):
		self.pop(Lexer.KW_JOIN)
		self.pop(Lexer.OP_PARENTHESES_LEFT)
		arrayofarrays = []
		while self.top()[0] != Lexer.OP_PARENTHESES_RIGHT:
			arrayofarrays.append(self.parseExpression())
			if self.top()[0] == Lexer.OP_COMMA:
				self.pop(Lexer.OP_COMMA)
		self.pop(Lexer.OP_PARENTHESES_RIGHT)
		return Join(arrayofarrays)

