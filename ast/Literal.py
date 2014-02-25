# -*- coding: utf-8 -*-
class Literal:
	""" Literal (tedy jakakoli konstanta, cislo). """
	def __init__(self, value):
		self.value = value
		self.type = "Literal"

	def __str__(self):
		return str(self.value)

	def run(self, frame,ff):
		return self.value