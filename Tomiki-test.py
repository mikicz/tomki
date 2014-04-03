# -*- coding: utf-8 -*-

import sys
sys.path.append('ast/')
from lexer import Lexer
# jmenuje se slparser (Simple Language Parser), aby se netriskal s pythonim modulem parser
from slparser import Parser
from ast import *
from bytecodeinterpret import BytecodeInterpret

def testLexer():
	""" Ukazka pouziti lexeru. """
	s = " append (bd fdfdg)"
	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali
	while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
		print(l.popToken())

def testParser():
	s = """/*
		function quicksort(seznam)
			{
				x = len(seznam);
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
		print b;
		print a;*/

		


# Left = index prvku nejvíc vlevo, Right = Index prvku nejvíc vpravo
function partition(seznam, left, right, pivotIndex) {
	temporary = seznam[len(seznam)-1];
	seznam[len(seznam)-1] = seznam[pivotIndex];	# Move pivot
	seznam[pivotIndex] = temporary;				# to end
	storeIndex = left;
	i = left;
	while (i <= right){
		if (seznam[i] <= seznam[pivotIndex]){
			temporary = seznam[i];
			seznam[i] = seznam[storeIndex]; # Swap storeIndex with i
			seznam[storeIndex] = temporary;
			storeIndex = storeIndex + 1;
		};
	temporary = seznam[storeIndex];
	seznam[storeIndex] = seznam[right];		#swap storeIndex with right
	seznam[right] = temporary;
	return storeIndex
	};
};

function quicksort-in-place(seznam, left, right){
	pivotIndex = len(seznam)//2;			#pivot někde uprostřed
	#	Get lists of bigger and smaller items and final position of pivot
	pivotNewIndex = partition(seznam, left, right, pivotIndex);
	# Recursively sort elements smaller than the pivot (assume pivotNewIndex - 1 does not underflow)
	quicksort(array, left, pivotNewIndex - 1);
	# Recursively sort elements at least as big as the pivot (assume pivotNewIndex + 1 does not overflow)
	quicksort(array, pivotNewIndex + 1, right);
};

a = [758,796,7,875,745,1,5,5,5,65,46,56,987,8765,46];
print a;
left = 0;
right = len(seznam)-1;
b = quicksort-in-place(a, left, right);
print b;

			"""
	#s = "a = 5; b = [a]; a = 6; print b; "
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

def testInterpret():
	s = """
	a = 5;
	b = 6;
	if ( a == b )
		{
			c = 7;
		}
	elif ( a > b )
		{
			c = 8;
		}
	elif ( a < b )
		{
			c = 9;
		}
	else
		{
			c = 10;
		};
	"""

	l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
	l.analyzeString(s) # timhle mu reknete, aby naparsoval string, ktery jste napsali

	p = Parser(l) # zalozim si parser a dam mu lexer ze ktereho bude cist tokeny
	ast = p.parse() # naparsuju co mam v lexeru a vratim AST 

	frame = Frame(None)
	ffy=FunctionFrame()
	print(ast) # zobrazim ten strom
	
	block = BytecodeInterpret()

	ast.compile(block)

	print block



testInterpret()