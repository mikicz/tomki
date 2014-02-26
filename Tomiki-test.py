# -*- coding: utf-8 -*-

import sys
sys.path.append('ast/')
from lexer import Lexer
# jmenuje se slparser (Simple Language Parser), aby se netriskal s pythonim modulem parser
from slparser import Parser
from ast import *

def testLexer():
	""" Ukazka pouziti lexeru. """
	s = " append (bd fdfdg)"
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
		print(l.popToken())

def testParser():
	s = """
		function quicksort(seznam)
			{
				if (len(seznam) <= 1)
					{
						return seznam;
					};
				pivot = pop(seznam,0);
				mali = [];
				velci = [];
				for prvek in seznam
					{
						if (prvek<pivot)
							{
								append(mali,prvek);
							}
						else
							{
								append(velci,prvek);
							};
					};
				vystup1 = quicksort(mali);
				vystup2 = quicksort(velci);
				vystup = vystup1+[pivot]+vystup2;
				return vystup;



			};
		a = [758,796,7,875,745,1,5,5,5,65,46,56,987,8765,46];
		b = quicksort(a);
		for i in b
			{
				c = i + " "
				print c;
			};
			"""
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