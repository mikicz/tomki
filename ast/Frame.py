# -*- coding: utf-8 -*-
from Literal import Literal
class Frame:

	def __init__(self,parent):
		self.locals =  {}
		self.parent = parent

	def set (self, name, value, functionFrame):
		try:
			if value.type=="Literal": #uloží se jenom literal, zbytek se nejdřív pustí, aby z toho vyšel literal
				self.locals[name] = value
			else:
				self.locals[name] = Literal(value.run(self, functionFrame))
		except:
			self.locals[name] = Literal(value)
		return Literal(True)

	def get (self, name):
		if (name in self.locals):
			return self.locals[name]
		if (self.parent == None): #pokud není rodič, nemůžu se podívat nahoru a tím pádem proměná neexistuje
			raise BaseException("Proměnná "+str(name)+" neexistuje")
		return self.parent.get(name)