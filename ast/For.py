# -*- coding: utf-8 -*-
from Frame import Frame
from VariableWrite import VariableWrite
from Literal import Literal
from copy import copy
class For:
	""" pamatuje si kam se má ukládat jednotlivý prvek seznamu, seznam a block
	KW_FOR ident KW_IN ( ident | FCALL | FIELD) BLOCK
	"""

	def __init__(self, variable, array, block):
		self.variable = variable
		self.array = array
		self.block = block
		self.type = "For"

	def __str__(self):
		return "for (%s) in %s %s" % (self.variable, self.array, self.block)

	def run(self, frame, ff):
		variableName = self.variable.run(frame,ff)
		array = self.array.run(frame,ff)

		for prvek in array:
			novyframe=Frame(frame)
			localblock = copy (self.block) #aby to neodkazovalo na stejný blok
			localblock.add_zacatek(VariableWrite(variableName,prvek))
			localblock.run(novyframe,ff)
