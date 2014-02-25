# -*- coding: utf-8 -*-

class FunctionFrame:

	def __init__(self):
		self.functions = {}

	def add (self, name, arrgs, block):
		self.functions[name] = [arrgs, block]

	def get (self, name):
		return self.functions[name]