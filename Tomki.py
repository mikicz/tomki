# -*- coding: utf-8 -*-
import sys
from lexer import Lexer
# jmenuje se slparser (Simple Language Parser), aby se netriskal s pythonim modulem parser
from slparser import Parser
from ast import *


filename = str(sys.argv[1])
file = open(filename, "r")
str = file.read()
file.close()

Lex = Lexer()
Lex.analyzeString(str)

Par = Parser(Lex)
AST = Par.parse()
print AST

frame = Frame(None)
AST.run(frame)

print frame.locals