from lexer import Lexer
# jmenuje se slparser (Simple Language Parser), aby se netriskal s pythonim modulem parser
from slparser import Parser


def testLexer():
	""" Ukazka pouziti lexeru. """
	s = " if (a == 4) { a = 2 + 3 } else { a = a + (b - 2) }"
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
		print(l.popToken())

def testParser():
	s = "x = 2 + 2; y = 3 + x"
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	p = Parser(l) # zalozim si parser a dam mu lexer ze ktereho bude cist tokeny
	ast = p.parse() # naparsuju co mam v lexeru a vratim AST 
	print(ast) # zobrazim ten strom
	ast.run()





testParser()