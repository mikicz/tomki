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
				x = len(seznam);
				if (x <= 1)
					{
						return seznam;
					}
				else
					{
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
						vystup = join (vystup1, pivot, vystup2);
						return vystup;
					};
			};
		a = [7,758,6,87,25465,487,654,87,564,687,65];
		b = quicksort(a);
		print b;
		
			"""
	"""s = 
		function rekurze(bla) 
			{
				if(bla<=0){
					return(bla);
				};
				print bla;
				bla = bla - 1;
				return( rekurze(bla) );
			}; 
		rekurze(10); """
#	s = """ 		bla = 5;		function nekdo(){			print("test");		};		nekdo();		print bla;"""
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali

	p = Parser(l) # zalozim si parser a dam mu lexer ze ktereho bude cist tokeny
	ast = p.parse() # naparsuju co mam v lexeru a vratim AST 

	frame = Frame(None)
	ffy=FunctionFrame()
	print(ast) # zobrazim ten strom
	ast.run(frame,ffy)
	print frame.locals
	#print ffy.functions





testParser()