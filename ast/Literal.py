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

	def run(self, frame, functionFrame, index=None):
		#print self.value
		try:
			if self.value.type == "Literal":
				self.value = self.value.run(frame, functionFrame)
		except:
			pass

		if index!=None:
			return self.value[index.run(frame, functionFrame)].run(frame, functionFrame)
		else:
			if (isinstance(self.value, list)):
				blah = []
				for i in self.value:
					try:
						blah.append(i.run(frame, functionFrame))
					except:
						blah.append(i)
				return blah
			return self.value