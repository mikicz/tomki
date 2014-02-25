# -*- coding: utf-8 -*-

class Frame:

	def __init__(self,parent):
		self.locals =  {}
		self.parent = parent

	def set (self, name, value):
		if hasattr(value, 'literal'): #uloží se jenom literal, zbytek se nejdřív pustí, aby z toho vyšel literal
			self.locals[name] = value
		else:
			self.locals[name] = value.run(self, None)

	def get (self, name):
		if (name in self.locals):
			return self.locals[name]
		if (self.parent == None): #pokud není rodič, nemůžu se podívat nahoru a tím pádem proměná neexistuje
			raise
		return self.parent.get(self.name)