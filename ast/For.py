# -*- coding: utf-8 -*-
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