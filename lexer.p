# -*- coding: utf-8 -*-
import sys

def isLetter(a):
	""" Funkce ktera zjisti, jestli dany znak je pismeno. Pismeno je bud male, nebo velke pismeno. """
	return ((a>='a') and (a<='z')) or ((a>='A') and (a<='Z'))

def isDigit(a):
	""" Funkce, ktera zjisti, jestli dany znak je cislice desitkove soustavy. """
	return (a>='0') and (a<='9')

def isWhitespace(a):
	""" Funkce, ktera zjisti, jestli dany znak je whitespace. Momentalne je whitespace mezera, tab a nebo novy radek. Opacna lomitka jsou ridici znaky, kterymi muzeme zapisovat specialni znaky, ktere nejsou na klavesnici. Takze \n je konec radky, a ne opacne lomitko a male n. To by se napsalo jako \\n."""
	return (a in (' ','\t', '\n'))

class Lexer:
	""" Lexikalni analyzator.
    
	Objekt, ktery se stara o lexikalni analyzu. Obsahuje v sobe vsechny druhy tokenu, a metody, ktere do tokenu umi prevest libovolny retezec. Kdyz se retezec prevede, tokeny se pridaji do seznamu tokenu. Kazdy token je tuple (typ tokenu, hodnota tokenu). Metody topToken() a popToken() slouzi k zobrazeni a posunuti se na dalsi token. Ty budeme pouzivat dale. 
    """

	EOF = "<EOF>" # typ token pro konec souboru, End Of File, oznacuje, ze uz neni zadny dalsi token za nim
	_EOF = (EOF, None) # tohle je token, je to tuple z typu, a hodnoty, hodnota EOF je zadna
	NUMBER = "number" # token pro cislo, jeho hodnotou bude hodnota cisla
	IDENT = "ident" # token pro identifikator, jeho hodnotou bude retezec s identifikatorem
	# tohle jsou jen ukazky operatoru a klicovych slov, vase budou vypadat podle toho, jak bude vypadat vas jazyk
	KW_IF = "if" # klicove slovo if 
	KW_ELSE = "else" # klicove slovo else
	OP_ADD = "+" # operator scitani
	OP_EQ = "==" # operator porovnani
	OP_ASSIGN = "=" # operator prirazeni


	def __init__(self):
		""" Inicializuje lexikalni analyzator. Zalozi pole tokenu, zalozi seznam klicovych slov, atd. """
		self._tokens = [] # seznam tokenu, ktere jsme uz naparsovali
		self._keywords = {} # seznam klicovych slov. Ulozena jsou jako [klicove slovo] = typ tokenu odpovidajici
		self._keywords["if"] = Lexer.KW_IF # takhle pridate vlastni klicova slova
		self._keywords["else"] = Lexer.KW_ELSE
		self._top = 0 # ukazatel na token ktery vrati funkce topToken() vysvetlime si pozdeji
		self._string = "" # aktualne zpracovavany retezec
		self._pos = 0 # pozice v aktualne zpracovavanem retezci

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
		print("Pri analyze doslo k chybe: ", reason)
		sys.exit(1)

	def addToken(self, tokenType, tokenValue = None):
		""" Funkce, ktera prida dany druh tokenu a pripadne i hodnotu na seznam jiz naparsovanych tokenu. Kdyz naparsujete nejaky token, musite zavolat tuhle funkci. """
		self._tokens.append((tokenType, tokenValue))

	def skipWhitespace(self):
		""" Preskoci whitespace v aktualne zpracovavanem retezci. """
		while (isWhitespace(self.topChar())):
			self.popChar()

	def parseNumber(self):
		""" Naparsuje cele cislo a jeho hodnotu. """
		value = 0
		if (not isDigit(self.topChar())):
			self.error("Zacatek cisla musi byt cislo")
		while (isDigit(self.topChar())):
			value = value * 10 + (ord(self.topChar()) - ord('0'))
			self.popChar()
		self.addToken(Lexer.NUMBER, value)
	
	def parseIdentifierOrKeyword(self):
		""" Naparsuje identifikator nebo klicove slovo. Identifikator ma typ IDENT a svuj nazev jako hodnotu. Klicove slovo hodnotu nema, a typ ma podle toho, co je zac. Klicove slovo je takovy identifikator, ktery je ve slovniku klicovych slov, ktery jste inicializovali v metode __init__ nahore. """
		i = self._pos
		if (not isLetter(self.topChar())):
			self.error("Identifikator musi zacinat pismenem")
		while (isLetter(self.topChar())):
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
		if (isLetter(c)):
			self.parseIdentifierOrKeyword()
		elif (isDigit(c)):
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
		elif (c == '\0'):
			pass
		else:
			self.error("Neznamy znak na vstupu!")


# Tohle je ukazka pouziti a testovani
l = Lexer() # timhle si zalozite objekt lexilaniho analyzatoru
l.analyzeString("4 if huhu 23 + == 3 ") # timhle mu reknete, aby naparsoval string, ktery jste napsali
while (not l.isEOF()): # tohle slouzi k vypsani vsech tokenu
	print(l.popToken())
