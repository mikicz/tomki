# -*- coding: utf-8 -*-
from Literal import Literal
class Array:
	def __init__(self,polozkypole):
		self.polozkypole = polozkypole
		self.type = "Array"

	def __str__(self):
		a = "["
		for i in self.polozkypole:
			if (a == "["):
				a += i.__str__()
			else:
				a += "," + i.__str__()
		a += "]"
		return a

	def run(self, frame, ff):
		self.spustenepole = []
		for i in self.polozkypole:
			i.run(frame, ff)
			self.spustenepole.append(i)
		return Literal(self.spustenepole)