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

	def run(self, frame,ff, index=None):
		#print self.value
		try:
			if self.value.type == "Literal":
				self.value = self.value.run(frame,ff)
		except:
			pass

		if index!=None:
			return self.value[index.run(frame, ff)].run(frame,ff)
		else:
			if (isinstance(self.value, list)):
				blah = []
				for i in self.value:
					try:
						blah.append(i.run(frame,ff))
					except:
						blah.append(i)
				return blah
			return self.value