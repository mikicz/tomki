# -*- coding: utf-8 -*-
import sys


class Lexer:
	""" Lexikalni analyzator.
    
	Objekt, ktery se stara o lexikalni analyzu. Obsahuje v sobe vsechny druhy tokenu,
	a metody, ktere do tokenu umi prevest libovolny retezec. Kdyz se retezec prevede,
	tokeny se pridaji do seznamu tokenu. Kazdy token je tuple (typ tokenu, hodnota
	tokenu). Metody topToken() a popToken() slouzi k zobrazeni a posunuti se na
	dalsi token. Ty budeme pouzivat dale. 
    """

	EOF = "<EOF>" # typ token pro konec souboru, End Of File, oznacuje, ze uz neni zadny dalsi token za nim
	_EOF = (EOF, None, None) # tohle je token, je to tuple z typu, a hodnoty, hodnota EOF je zadna
	NUMBER = "number" # token pro cislo, jeho hodnotou bude hodnota cisla
	STRING = "string"
	IDENT = "ident" # token pro identifikator, jeho hodnotou bude retezec s identifikatorem
	# tohle jsou jen ukazky operatoru a klicovych slov, vase budou vypadat podle toho, jak bude vypadat vas jazyk

	#keywords
	KW_IF = "if" # klicove slovo if 
	KW_ELSE = "else" # klicove slovo else
	KW_ELIF = "elif"
	KW_WHILE = "while"
	KW_FOR = "for"
	KW_IN = "in"
	KW_BREAK = "break"
	KW_CONTINUE = "continue"
	KW_RETURN = "return"
	KW_FUNCTION = "function"
	KW_PRINT = "print"

	#operace
	OP_ADD = "+" # operator scitani
	OP_EQUAL = "==" # operator porovnani
	OP_ASSIGN = "=" # operator prirazeni
	OP_SUBSTRACT = "-" # operátor mínus
	OP_MULTIPLY = "*" # operátor násobení
	OP_DIVIDE = "/" # operátor dělení
	OP_MOCNIT = "^" # operátor mocnění, nevím jak se to řekne česky, může to být: ^ a **
	OP_FLOORDIVISION = "//" # operátor dělení, který ale bude floorovaný (9//2=4)
	OP_REMAINDER = "%" # operátor zbytku po dělení
	OP_AND = "and" # a to: and AND &
	OP_OR = "or" # a to: or OR 
	OP_NOT = "not" # a to: not NOT
	OP_NOTEQUAL = "<>" # nebo i !=
	OP_BIGGER = ">"
	OP_SMALLER = "<"
	OP_BIGGEROREQUAL = ">="
	OP_SMALLEROREQUAL = "<="
	OP_PARENTHESES_LEFT = "("
	OP_PARENTHESES_RIGHT = ")"
	OP_BRACES_LEFT = "{"
	OP_BRACES_RIGHT = "}"
	OP_BRACKETS_LEFT = "["
	OP_BRACKETS_RIGHT = "]"
	OP_COMMA = ","
	OP_SEMICOLON = ";"

	OP_QUOTATION_MARK = "\""
	OP_APOSTROPHE = "'"


	

	def __init__(self):
		""" Inicializuje lexikalni analyzator. Zalozi pole tokenu, zalozi seznam klicovych slov, atd. """
		self._tokens = [] # seznam tokenu, ktere jsme uz naparsovali
		self._keywords = {} # seznam klicovych slov. Ulozena jsou jako [klicove slovo] = typ tokenu odpovidajici
		self.currentline = 1 # počítadlo současného řádku do chybového hlášení
		self.currentcolumn = 1 #počítadlo současného znaku
		self.skonciuzkurva = 0 # nějak to nechtělo skončit, tak jsem to udělal takhle

		#klíčová slova
		self._keywords["if"] = Lexer.KW_IF 
		self._keywords["else"] = Lexer.KW_ELSE
		self._keywords["elif"] = Lexer.KW_ELIF
		self._keywords["while"] = Lexer.KW_WHILE
		self._keywords["for"] = Lexer.KW_FOR
		self._keywords["in"] = Lexer.KW_IN
		self._keywords["break"] = Lexer.KW_BREAK
		self._keywords["continue"] = Lexer.KW_CONTINUE
		self._keywords["return"] = Lexer.KW_RETURN
		self._keywords["function"] = Lexer.KW_FUNCTION
		self._keywords["print"] = Lexer.KW_PRINT

		self._keywords["and"] = Lexer.OP_AND
		self._keywords["or"] = Lexer.OP_OR
		self._keywords["not"] = Lexer.OP_NOT

		self._top = 0 # ukazatel na token ktery vrati funkce topToken() vysvetlime si pozdeji
		self._string = "" # aktualne zpracovavany retezec
		self._pos = 0 # pozice v aktualne zpracovavanem retezci


# Funkce na šťování znaků
	def isLetter(self, a):
		""" Funkce ktera zjisti, jestli dany znak je pismeno. Pismeno je bud male, nebo velke pismeno. """
		return ((a>='a') and (a<='z')) or ((a>='A') and (a<='Z'))

	def isDigit(self, a):
		""" Funkce, ktera zjisti, jestli dany znak je cislice desitkove soustavy. """
		return (a>='0') and (a<='9')

	def isWhitespace(self, a):
		"""
		Funkce, ktera zjisti, jestli dany znak je whitespace. Momentalne je
		whitespace mezera, tab a nebo novy radek. Opacna lomitka jsou ridici znaky,
		kterymi muzeme zapisovat specialni znaky, ktere nejsou na klavesnici.
		Takze \n je konec radky, a ne opacne lomitko a male n. To by se napsalo jako \\n.
		"""

		if (a == "\n"):
			self.currentline += 1
			self.currentcolumn = 1
		return (a in (' ','\t', '\n'))

	def isBinary(self, a):
		""" Funkce, která zjisti, jestli je daný znak číslice binární soustavy. """
		return ((a=="0") or (a=="1"))

	def isHexadecimal(self, a):
		""" Funkce, která zjisti, jestli je daný znak číslice hexidecimální soustavy. """
		return ((a>='0') and (a<='9')) or ((a>="A") and (a<="F")) or ((a>="a") and (a<="f"))

	def topToken(self, i = 0):
		""" Vrati aktualni token. Vysvetlime si priste. """
		if (self._top < len(self._tokens)):
			return self._tokens[ self._top  + i ]
		else:
			return Lexer._EOF

	def popToken(self, value=None):
		""" Posune se na dalsi token. Vysvetlime priste. """
		t = self.topToken()
		if (self._top < len(self._tokens) and (value == None or value == t[0])):
			self._top += 1
		else:
			self.error("Očekáván jiný typ tokenu")
		return t

	def isEOF(self):
		""" Vrati true, jestlize uz zadne dalsi tokeny nejsou. Vysvetlime si priste. """
		return self._top >= len(self._tokens)


	def topChar(self, value = 1):
		""" Vrati aktualne zpracovavany znak. Tohle je funkce jen proto, abychom
		nemuseli porad psat ten slozity pristup. """
		return self._string[self._pos:self._pos + value]

	def popChar(self, value = 1):
		"""
		Posune nas na dalsi znak v aktualne analyzovanem retezci, pokud takovy
		existuje. Zase funkce pro prehlednost, abychom nemuseli mit to kontrolovani
		mezi vsude.
		"""
		if (self._pos < len(self._string)):
			self._pos += value
			self.currentcolumn += value

	def error(self, reason):
		""" Funkce pro prehlednost, vypise ze doslo k chybe, k jake chybe doslo, a skonci program. """
		print("Pri analyze doslo na radku "+str(self.currentline)+" cca v sloupci "+str(self.currentcolumn)+" k chybe z duvodu: ", reason)
		sys.exit(1)

	def addToken(self, tokenType, tokenValue = None, tokenLine = None):
		"""
		Funkce, ktera prida dany druh tokenu a pripadne i hodnotu na seznam jiz
		naparsovanych tokenu. Kdyz naparsujete nejaky token, musite zavolat tuhle
		funkci.
		"""
		self._tokens.append((tokenType, tokenValue, tokenLine))

	def skipWhitespace(self):
		""" Preskoci whitespace v aktualne zpracovavanem retezci. """
		while (self.isWhitespace(self.topChar())):
			self.popChar()

# funkce na parsování tokenů
	def parseNumber(self):
		""" Naparsuje cislo v desitkove soustave a jeho hodnotu. """
		value = 0
		if (not self.isDigit(self.topChar())):
			self.error("Zacatek cisla musi byt cislo")
		while (self.isDigit(self.topChar())):
			value = value * 10 + (ord(self.topChar()) - ord('0'))
			self.popChar()

		if (self.topChar()=="."):
			self.popChar()
			if (not self.isDigit(self.topChar())):
				self.error("Po desetine tecce musi byt aspon jedno cislo")
			value = float(value)
			x=10.0
			value = value + (ord(self.topChar()) - ord('0'))/x
			self.popChar()
			while (self.isDigit(self.topChar())):
				x = x * 10
				value = value + (ord(self.topChar()) - ord('0'))/x
				self.popChar()

		self.addToken(Lexer.NUMBER, value, self.currentline)

	def parseBinaryNumber(self):
		""" Naparsuje binární číslo a jeho hodnotu. """
		value = 0
		if (not self.isBinary(self.topChar())):
			self.error("Zacatek cisla musi byt binarni cislo")
		while (self.isDigit(self.topChar())):
			value = value * 2 + (ord(self.topChar()) - ord('0'))
			self.popChar()
		self.addToken(Lexer.NUMBER, value, self.currentline)

	def parseHexadecimalNumber(self):
		""" Naparsuje hexadecimální číslo a jeho hodnotu. """
		value = 0
		if (not self.isHexadecimal(self.topChar())):
			self.error("Zacatek cisla musi byt hexadecimalni cislo")
		while (self.isHexadecimal(self.topChar())):

			x=self.topChar()
			if ((x>='0') and (x<='9')):
				y=ord(x)-ord('0')
			else:
				if (x=="A") or (x=="a"):
					y=10
				elif (x=="B") or (x=="b"):
					y=11
				elif (x=="C") or (x=="c"):
					y=12
				elif (x=="D") or (x=="d"):
					y=13
				elif (x=="E") or (x=="e"):
					y=14
				elif (x=="F") or (x=="f"):
					y=15
				else:
					self.error("Hexadecimalni cislo s nehexadecimalnimi znaky")
				
			value = value * 16 + y
			self.popChar()
		self.addToken(Lexer.NUMBER, value, self.currentline)

	def parseString(self, zacatek):
		""" Naparsuje string """
		value = ""
		while (self.topChar()!=zacatek):
			value += self.topChar()
			self.popChar()
		self.popChar()
		self.addToken(Lexer.STRING, value, self.currentline)



	
	def parseIdentifierOrKeyword(self):
		"""
		Naparsuje identifikator nebo klicove slovo. Identifikator ma typ IDENT
		a svuj nazev jako hodnotu. Klicove slovo hodnotu nema, a typ ma podle toho,
		co je zac. Klicove slovo je takovy identifikator, ktery je ve slovniku
		klicovych slov, ktery jste inicializovali v metode __init__ nahore.
		"""
		i = self._pos
		if (not self.isLetter(self.topChar())):
			self.error("Identifikator musi zacinat pismenem")
		while (self.isLetter(self.topChar()) or self.isDigit(self.topChar())):
			self.popChar()
		value = self._string[i : self._pos].lower()
		if (value in self._keywords):
			self.addToken(self._keywords[value], None, self.currentline)
		else:
			self.addToken(Lexer.IDENT, value, self.currentline)

	
	def analyzeString(self, string):
		""" Rozkouskuje dany retezec na tokeny. Nastavi aktualne zpracovavany
		retezec na ten co funkci posleme, vynuluje aktualni pozici a vola funkci
		pro naparsovani tokenu dokuc neni cely retezec analyzovan. """
		self._string = string + "\0" # na konec retezce pridame znak s kodem 0
									 # (to neni 0 jako cifra, ale neviditelny znak).
									 # Ten se nesmi v retezci vyskytovat a my s
									 # nim jednoduse poznavame, ze jsme na konci. 
		self._pos = 0
		while (self._pos < len(self._string) and self.skonciuzkurva==0):
			self.parseToken()


	def parseToken(self):
		""" Naparsuje jeden token ze vstupniho retezce. Preskoci whitespace a pak
		se rozhodne jestli se jedna o cislo, identifikator, klicove slovo, operator,
		atd. a overi ze je vse v poradku. Token prida do seznamu naparsovanych tokenu. """
		self.skipWhitespace()
		c = self.topChar()
#		print c
		if (self.isLetter(c)):
			self.parseIdentifierOrKeyword()

		elif (self.isDigit(c)):
			self.parseNumber()

#Operátory
		elif (c == '+'):
			self.popChar()
			self.addToken(Lexer.OP_ADD, None, self.currentline)

		elif (c == '='):
			self.popChar()
			c = self.topChar()
			if (c == '='):
				self.popChar()
				self.addToken(Lexer.OP_EQUAL, None, self.currentline)
			else:
				self.addToken(Lexer.OP_ASSIGN, None, self.currentline)

		elif (c == '-'):
			self.popChar()
			self.addToken(Lexer.OP_SUBSTRACT, None, self.currentline)

		elif (c == '*'):
			self.popChar()
			c = self.topChar()
			if (c == '*'):
				self.popChar()
				self.addToken(Lexer.OP_MOCNIT, None, self.currentline)
			else:
				self.addToken(Lexer.OP_MULTIPLY, None, self.currentline)

		elif (c == "/"):
			self.popChar()
			c = self.topChar()
			if (c == '/'):
				self.popChar()
				self.addToken(Lexer.OP_FLOORDIVISION, None, self.currentline)
			elif (c == "*"):				# /* Komentář */
				self.popChar()
				while not(self.topChar() == "*" and self._string[self._pos+1] == "/"):
					self.popChar()
				self.popChar(2)
			else:
				self.addToken(Lexer.OP_DIVIDE, None, self.currentline)

		elif (c == "^"):
			self.popChar()
			self.addToken(Lexer.OP_MOCNIT, None, self.currentline)

		elif (c == "&"):
			self.popChar()
			self.addToken(Lexer.OP_AND, None, self.currentline)

		elif (c == "||"):
			self.popChar()
			self.addToken(Lexer.OP_OR, None, self.currentline)

		elif (c == "!"):
			self.popChar()
			c = self.topChar()
			if (c == '='):
				self.popChar()
				self.addToken(Lexer.OP_NOTEQUAL, None, self.currentline)
			else:
				self.addToken(Lexer.OP_NOT, None, self.currentline)

		elif (c == "%"):
			self.popChar()
			self.addToken(Lexer.OP_REMAINDER, None, self.currentline)

		elif (c == ">"):
			self.popChar()
			c = self.topChar()
			if (c == '='):
				self.popChar()
				self.addToken(Lexer.OP_BIGGEROREQUAL, None, self.currentline)
			else:
				self.addToken(Lexer.OP_BIGGER, None, self.currentline)

		elif (c == "<"):
			self.popChar()
			c = self.topChar()
			if (c == '='):
				self.popChar()
				self.addToken(Lexer.OP_SMALLEROREQUAL, None, self.currentline)
			elif (c == ">"):
				self.popChar
				self.addToken(Lexer.OP_NOTEQUAL, None, self.currentline)
			else:
				self.addToken(Lexer.OP_SMALLER, None, self.currentline)

# Závorky
		elif (c == "("):
			self.popChar()
			self.addToken(Lexer.OP_PARENTHESES_LEFT, None, self.currentline)
		elif (c == ")"):
			self.popChar()
			self.addToken(Lexer.OP_PARENTHESES_RIGHT, None, self.currentline)
		elif (c == "{"):
			self.popChar()
			self.addToken(Lexer.OP_BRACES_LEFT, None, self.currentline)
		elif (c == "}"):
			self.popChar()
			self.addToken(Lexer.OP_BRACES_RIGHT, None, self.currentline)
		elif (c == "["):
			self.popChar()
			self.addToken(Lexer.OP_BRACKETS_RIGHT, None, self.currentline)
		elif (c == "]"):
			self.popChar()
			self.addToken(Lexer.OP_BRACKETS_LEFT, None, self.currentline)

		elif (c == ","):
			self.popChar()
			self.addToken(Lexer.OP_COMMA, None, self.currentline)
		elif (c == ";"):
			self.popChar()
			self.addToken(Lexer.OP_SEMICOLON, None, self.currentline)

# Typy čísel
		elif (c == "$"):
			self.popChar()
			if self.topChar() == "b":
				self.popChar()
				self.parseBinaryNumber()
			elif self.topChar() == "h":
				self.popChar()
				self.parseHexadecimalNumber()
			elif self.topChar() == "d":
				self.popChar()
				self.parseNumber()
			else:
				self.error("Neznamy typ cisla")

		elif (c == "#"):	# komentář
			self.popChar()
			while self.topChar() != "\n":
				self.popChar()

		elif (c == "\""): # string
			self.popChar()
			self.parseString("\"")

		elif (c == "'"): # druhá varianta stringu
			self.popChar()
			self.parseString("'")



		elif (c == '\0'):
			self.addToken(Lexer._EOF)
			self.skonciuzkurva = 1 # aby to už kurva skončilo, nějak nefungovalo to počítadlo pozice a nechtělo se mi to říkat

		else:
			self.error("Neznamy znak na vstupu! Znak: "+c)

"""
# Tohle je ukazka pouziti a testovani
l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
string = pokus Test $b10110 

l.analyzeString(string) # timhle mu reknete, aby naparsoval string, ktery jste napsali
while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
	print(l.popToken())
"""