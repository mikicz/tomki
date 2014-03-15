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
				print "funguju";
				x = len(seznam);
				print "funguju 2";
				if (x == 1)
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
		a = [7,758,6];
		b = quicksort(a);
		print len(b);
		for x in b
			{
				print x;
			};
		
			"""
	s = """
		function rekurze(bla) 
			{
				print bla;
				x = bla + 1;
				rekurze(x);
			}; 
		rekurze(0); """
	#s = """ function neco (bla) { return 3+5; };  print neco(1);"""
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