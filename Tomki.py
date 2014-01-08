# -*- coding: utf-8 -*-
import sys
from lexer import Lexer
# jmenuje se slparser (Simple Language Parser), aby se netriskal s pythonim modulem parser
from slparser import Parser
from ast import *

def Tomki():
	filename = sys.argv[1]
	file = open(filename, "r")
	string = file.read()
	file.close()

	Lex = Lexer()
	Lex.analyzeString(string)

	Par = Parser(Lex)
	AST = Par.parse()

	frame = Frame(None)
	AST.run(frame)

Tomki()