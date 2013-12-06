# -*- coding: utf-8 -*-
class Frame:

	def __init__(self,parent):
		self.locals =  {}
		self.parent

	def set (self, name, value):
		self.locals[name] = value

	def get (self, name):
		if (name in self.locals):
			return self.locals[name]
		if (self.parent == None):
			pass
			#vyhoď error
		return self.parent.get(self.name)
