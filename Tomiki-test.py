from lexer import Lexer
# jmenuje se slparser (Simple Language Parser), aby se netriskal s pythonim modulem parser
from slparser import Parser
from ast import *

def testLexer():
	""" Ukazka pouziti lexeru. """
	s = " if (a == 4) { a = 2 + 3 } else { a = a + (b - 2) }"
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
		print(l.popToken())

def testParser():
	s = """function secti(a,b)
			{
				c = a + b;
				return c;
			};
			x = secti(1, 3);
			print (x);"""
	#s = """ a = 5; b = a + 3;"""
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali

	p = Parser(l) # zalozim si parser a dam mu lexer ze ktereho bude cist tokeny
	ast = p.parse() # naparsuju co mam v lexeru a vratim AST 

	frame = Frame(None)
	ffy=FunctionFrame()
	print(ast) # zobrazim ten strom
	ast.run(frame,ffy)
	print frame.locals
	print ffy.functions





testParser()