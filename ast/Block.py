# -*- coding: utf-8 -*-
class Block:
	""" Blok prikazu. 

	Nejedna se o nic jineho, nez o seznam prikazu, ktere jdou po sobe. 
	"""

	def __init__(self):
		self.code = []

	def add(self, node):
		""" Prida novy prikaz. """
		self.code.append(node)

	def add_zacatek(self,node):
		""" Přidá nový příkaz na začátek bloku"""
		self.code = [node] + self.code

	def __str__(self):
		self.result = "{"
		for node in self.code:
			self.result = self.result + "\n" + node.__str__()
		self.result = self.result + "\n}\n"
		return self.result

	def run(self, frame,ff):
		for prikaz in self.code:
			if (prikaz.type!="Return"):
				prikaz.run(frame,ff)
			else:
				return prikaz.run(frame,ff)	