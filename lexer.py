# -*- coding: utf-8 -*-
import sys

	

class Lexer:
	""" Lexikalni analyzator.
    
	Objekt, ktery se stara o lexikalni analyzu. Obsahuje v sobe vsechny druhy tokenu, a metody, ktere do tokenu umi prevest libovolny retezec. Kdyz se retezec prevede, tokeny se pridaji do seznamu tokenu. Kazdy token je tuple (typ tokenu, hodnota tokenu). Metody topToken() a popToken() slouzi k zobrazeni a posunuti se na dalsi token. Ty budeme pouzivat dale. 
    """

	EOF = "<EOF>" # typ token pro konec souboru, End Of File, oznacuje, ze uz neni zadny dalsi token za nim
	_EOF = (EOF, None) # tohle je token, je to tuple z typu, a hodnoty, hodnota EOF je zadna
	NUMBER = "number" # token pro cislo, jeho hodnotou bude hodnota cisla
	IDENT = "ident" # token pro identifikator, jeho hodnotou bude retezec s identifikatorem
	# tohle jsou jen ukazky operatoru a klicovych slov, vase budou vypadat podle toho, jak bude vypadat vas jazyk

	#keywords
	KW_IF = "if" # klicove slovo if 
	KW_ELSE = "else" # klicove slovo else
	KW_ELIF = "elif"
	KW_WHILE = "while"
	KW_FOR = "for"
	KW_BREAK = "break"
	KW_CONTINUE = "continue"
	KW_RETURN = "return"
	KW_FUNCTION = "function"

	#operace
	OP_ADD = "+" # operator scitani
	OP_EQ = "==" # operator porovnani
	OP_ASSIGN = "=" # operator prirazeni
	OP_SUBSTRACT = "-" # operátor mínus
	OP_MULTIPLY = "*" # operátor násobení
	OP_DIVIDE = "/" # operátor dělení
	OP_MOCNIT = "^" # operátor mocnění, nevím jak se to řekne česky, může to být: ^ a **
	OP_FLOORDIVISION = "//" # operátor dělení, který ale bude floorovaný (9//2=4)
	OP_REMAINDER = "%" # operátor zbytku po dělení
	OP_AND = "AND" # a to: and AND &
	OP_OR = "OR" # a to: or OR 
	OP_NOT = "NOT" # a to: not NOT
	OP_NOTEQUAL = "<>"
	OP_BIGGER = ">"
	OP_SMALLER = "<"
	OP_BIGGEROREQUAL = ">="
	OP_SMALLERORERUAL = "<="


	

	def __init__(self):
		""" Inicializuje lexikalni analyzator. Zalozi pole tokenu, zalozi seznam klicovych slov, atd. """
		self._tokens = [] # seznam tokenu, ktere jsme uz naparsovali
		self._keywords = {} # seznam klicovych slov. Ulozena jsou jako [klicove slovo] = typ tokenu odpovidajici
		self.soucasnyradek = 1 # počítadlo současného řádku do chybového hlášení

		#klíčová slova
		self._keywords["if"] = Lexer.KW_IF 
		self._keywords["else"] = Lexer.KW_ELSE
		self._keywords["elif"] = Lexer.KW_ELIF
		self._keywords["while"] = Lexer.KW_WHILE
		self._keywords["for"] = Lexer.KW_FOR
		self._keywords["break"] = Lexer.KW_BREAK
		self._keywords["continue"] = Lexer.KW_CONTINUE
		self._keywords["return"] = Lexer.KW_RETURN
		self._keywords["function"] = Lexer.KW_FUNCTION

		self._top = 0 # ukazatel na token ktery vrati funkce topToken() vysvetlime si pozdeji
		self._string = "" # aktualne zpracovavany retezec
		self._pos = 0 # pozice v aktualne zpracovavanem retezci

	def isLetter(self, a):
		""" Funkce ktera zjisti, jestli dany znak je pismeno. Pismeno je bud male, nebo velke pismeno. """
		return ((a>='a') and (a<='z')) or ((a>='A') and (a<='Z'))

	def isDigit(self, a):
		""" Funkce, ktera zjisti, jestli dany znak je cislice desitkove soustavy. """
		return (a>='0') and (a<='9')

	def isWhitespace(self, a):
		""" Funkce, ktera zjisti, jestli dany znak je whitespace. Momentalne je whitespace mezera, tab a nebo novy radek. Opacna lomitka jsou ridici znaky, kterymi muzeme zapisovat specialni znaky, ktere nejsou na klavesnici. Takze \n je konec radky, a ne opacne lomitko a male n. To by se napsalo jako \\n."""
		#if (a == "\n"):
		#	self.soucasnyradek+=1
		return (a in (' ','\t', '\n'))


	def topToken(self):
		""" Vrati aktualni token. Vysvetlime si priste. """
		if (self._top < len(self._tokens)):
			return self._tokens[self._top]
		else:
			return Lexer._EOF

	def popToken(self):
		""" Posune se na dalsi token. Vysvetlime priste. """
		t = self.topToken()
		if (self._top < len(self._tokens)):
			self._top += 1
		return t

	def isEOF(self):
		""" Vrati true, jestlize uz zadne dalsi tokeny nejsou. Vysvetlime si priste. """
		return self._top >= len(self._tokens)

	def topChar(self):
		""" Vrati aktualne zpracovavany znak. Tohle je funkce jen proto, abychom nemuseli porad psat ten slozity pristup. """
		return self._string[self._pos]

	def popChar(self):
		""" Posune nas na dalsi znak v aktualne analyzovanem retezci, pokud takovy existuje. Zase funkce pro prehlednost, abychom nemuseli mit to kontrolovani mezi vsude. """
		if (self._pos < len(self._string)):
			self._pos += 1

	def error(self, reason):
		""" Funkce pro prehlednost, vypise ze doslo k chybe, k jake chybe doslo, a skonci program. """
		print("Při analýze došlo na řádku"+self.soucasnyradek+" k chybě z důvodu: ", reason)
		sys.exit(1)

	def addToken(self, tokenType, tokenValue = None):
		""" Funkce, ktera prida dany druh tokenu a pripadne i hodnotu na seznam jiz naparsovanych tokenu. Kdyz naparsujete nejaky token, musite zavolat tuhle funkci. """
		self._tokens.append((tokenType, tokenValue))

	def skipWhitespace(self):
		""" Preskoci whitespace v aktualne zpracovavanem retezci. """
		while (self.isWhitespace(self.topChar())):
			self.popChar()

	def parseNumber(self):
		""" Naparsuje cele cislo a jeho hodnotu. """
		value = 0
		if (not self.isDigit(self.topChar())):
			self.error("Zacatek cisla musi byt cislo")
		while (self.isDigit(self.topChar())):
			value = value * 10 + (ord(self.topChar()) - ord('0'))
			self.popChar()
		self.addToken(Lexer.NUMBER, value)

	def parseBinaryNumber(self):
		""" Naparsuje binární číslo a jeho hodnotu. """
		value = 0
		if (not self.isDigit(self.topChar())):
			self.error("Začátek čísla musí být číslo")
		while (self.isDigit(self.topChar())):
			value = value * 2 + (ord(self.topChar()) - ord('0'))
			self.popChar()
		self.addToken(Lexer.NUMBER, value)

	
	def parseIdentifierOrKeyword(self):
		""" Naparsuje identifikator nebo klicove slovo. Identifikator ma typ IDENT a svuj nazev jako hodnotu. Klicove slovo hodnotu nema, a typ ma podle toho, co je zac. Klicove slovo je takovy identifikator, ktery je ve slovniku klicovych slov, ktery jste inicializovali v metode __init__ nahore. """
		i = self._pos
		if (not self.isLetter(self.topChar())):
			self.error("Identifikator musi zacinat pismenem")
		while (self.isLetter(self.topChar())):
			self.popChar()
		value = self._string[i : self._pos]
		if (value in self._keywords):
			self.addToken(self._keywords[value])
		else:
			self.addToken(Lexer.IDENT, value)

	
	def analyzeString(self, string):
		""" Rozkouskuje dany retezec na tokeny. Nastavi aktualne zpracovavany retezec na ten co funkci posleme, vynuluje aktualni pozici a vola funkci pro naparsovani tokenu dokuc neni cely retezec analyzovan. """
		self._string = string + "\0" # na konec retezce pridame znak s kodem 0 (to neni 0 jako cifra, ale neviditelny znak). Ten se nesmi v retezci vyskytovat a my s nim jednoduse poznavame, ze jsme na konci. 
		self._pos = 0
		while (self._pos < len(self._string)):
			self.parseToken()

	def parseToken(self):
		""" Naparsuje jeden token ze vstupniho retezce. Preskoci whitespace a pak se rozhodne jestli se jedna o cislo, identifikator, klicove slovo, operator, atd. a overi ze je vse v poradku. Token prida do seznamu naparsovanych tokenu. """
		self.skipWhitespace()
		c = self.topChar()
		if (self.isLetter(c)):
			self.parseIdentifierOrKeyword()

		elif (self.isDigit(c)):
			self.parseNumber()

		elif (c == '+'):
			self.popChar()
			self.addToken(Lexer.OP_ADD)

		elif (c == '='):
			self.popChar()
			c = self.topChar()
			if (c == '='):
				self.popChar()
				self.addToken(Lexer.OP_EQ)
			else:
				self.addToken(Lexer.OP_ASSIGN)

		elif (c == '-'):
			self.popChar()
			self.addToken(Lexer.OP_SUBSTRACT)

		elif (c == '*'):
			self.popChar()
			c = self.topChar()
			if (c == '*'):
				self.popChar()
				self.addToken(Lexer.OP_MOCNIT)
			else:
				self.addToken(Lexer.OP_MULTIPLY)

		elif (c == "/"):
			self.popChar()
			c = self.topChar()
			if (c == '/'):
				self.popChar()
				self.addToken(Lexer.OP_FLOORDIVISION)
			else:
				self.addToken(Lexer.OP_DIVIDE)

		elif (c == "^"):
			self.popChar()
			self.addToken(LEXER.OP_MOCNIT)

		elif (c == "%"):
			self.popChar()
			self.addToken(LEXER.OP_REMAINDER)

		elif (c == ">"):
			self.popChar()
			c = self.topChar()
			if (c == '='):
				self.popChar()
				self.addToken(Lexer.OP_BIGGEROREQUAL)
			else:
				self.addToken(Lexer.OP_BIGGER)

		elif (c == "<"):
			self.popChar()
			c = self.topChar()
			if (c == '='):
				self.popChar()
				self.addToken(Lexer.OP_SMALLEROREQUAL)
			else:
				self.addToken(Lexer.OP_SMALLER)


		elif (c == '\0'):
			pass

		else:
			self.error("Neznamy znak na vstupu!")


# Tohle je ukazka pouziti a testovani
l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
l.analyzeString("4 if huhu 23 + == 3 ") # timhle mu reknete, aby naparsoval string, ktery jste napsali
while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
	print(l.popToken())
