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
	s = "x = 3; y = 1;  if ( x == 1) { y = y + 1} elif ( x == 2) { y = y + 2} elif (x == 3) { y = y + 4}  else { y = y + 3} "
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	p = Parser(l) # zalozim si parser a dam mu lexer ze ktereho bude cist tokeny
	ast = p.parse() # naparsuju co mam v lexeru a vratim AST 
	frame = Frame(None)
	print(ast) # zobrazim ten strom
	ast.run(frame)
	print frame.locals





testParser()