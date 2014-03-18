# -*- coding: utf-8 -*-
class While:
	""" Pamatuje si podmínku a blok, který opakuje 
	KW_WHILE '(' E ')' BLOCK
	 """

	def __init__(self, condition, block):
		self.condition = condition
		self.block = block
		self.type = "While"

	def __str__(self):
		return "while (%s) %s" % (self.condition, self.block)

	def run(self, frame, functionFrame):
		while self.condition.run(frame, functionFrame) == True:
			self.block.run(frame, functionFrame)