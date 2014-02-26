# -*- coding: utf-8 -*-
class Append:
	def __init__(self, ident, value):
		self.ident = ident
		self.value = value
		self.type = "Append"
	def __str__(self):
		return "append (%s, %s)" % (self.ident, self.value)

	def run(self, frame, ff):
		print "získávám array"
		self.array = frame.get(self.ident).run(frame,ff)
		print self.array
		self.array.append(self.value)
		print "vracím array"
		return frame.set(self.ident,self.array, ff)