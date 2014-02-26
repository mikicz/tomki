# -*- coding: utf-8 -*-
class Literal:
	""" Literal (tedy jakakoli konstanta, cislo, seznam). """
	def __init__(self, value):
		self.value = value
		self.type = "Literal"

	def __str__(self):
		try:
			a = self.value[0]
			return "Je tady pole a nefunguje mi kurva debilni __str__"

		except:
			return str(self.value)

	def run(self, frame,ff, index=None):
		if index!=None:
			return self.value[index.run(frame, ff)].run(frame,ff)
		else:
			return self.value