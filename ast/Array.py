# -*- coding: utf-8 -*-
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
		return self.polozkypole
