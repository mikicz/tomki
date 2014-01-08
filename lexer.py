�
���Rc           @   s#   d  d l  Z  d f  d �  �  YZ d S(   i����Nt   Lexerc           B   s�  e  Z d  Z d Z e d= d= f Z d Z d Z d Z d Z	 d Z
 d Z d Z d	 Z d
 Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z d Z  d Z! d Z" d Z# d  Z$ d! Z% d" Z& d# Z' d$ Z( d% Z) d& Z* d' �  Z+ d( �  Z, d) �  Z- d* �  Z. d+ �  Z/ d, �  Z0 d- d. � Z1 d= d/ � Z2 d0 �  Z3 d1 d2 � Z4 d1 d3 � Z5 d4 �  Z6 d= d= d5 � Z7 d6 �  Z8 d7 �  Z9 d8 �  Z: d9 �  Z; d: �  Z< d; �  Z= d< �  Z> RS(>   s�   Lexikalni analyzator.
    
	Objekt, ktery se stara o lexikalni analyzu. Obsahuje v sobe vsechny druhy tokenu,
	a metody, ktere do tokenu umi prevest libovolny retezec. Kdyz se retezec prevede,
	tokeny se pridaji do seznamu tokenu. Kazdy token je tuple (typ tokenu, hodnota
	tokenu). Metody topToken() a popToken() slouzi k zobrazeni a posunuti se na
	dalsi token. Ty budeme pouzivat dale. 
    s   <EOF>t   numbert   identt   ift   elset   elift   whilet   fort   int   breakt   continuet   returnt   functiont   +s   ==t   =t   -t   *t   /t   ^s   //t   %t   andt   ort   nots   <>t   >t   <s   >=s   <=t   (t   )t   {t   }t   [t   ]t   ,t   ;c         C   s  g  |  _  i  |  _ d |  _ d |  _ d |  _ t j |  j d <t j |  j d <t j |  j d <t j	 |  j d <t j
 |  j d <t j |  j d <t j |  j d	 <t j |  j d
 <t j |  j d <t j |  j d <t j |  j d <t j |  j d <t j |  j d <d |  _ d |  _ d |  _ d S(   s[    Inicializuje lexikalni analyzator. Zalozi pole tokenu, zalozi seznam klicovych slov, atd. i   i    R   R   R   R   R   R   R	   R
   R   R   R   R   R   t    N(   t   _tokenst	   _keywordst   currentlinet   currentcolumnt   skonciuzkurvaR    t   KW_IFt   KW_ELSEt   KW_ELIFt   KW_WHILEt   KW_FORt   KW_INt   KW_BREAKt   KW_CONTINUEt	   KW_RETURNt   KW_FUNCTIONt   OP_ANDt   OP_ORt   OP_NOTt   _topt   _stringt   _pos(   t   self(    (    s$   /home/tom/Development/Tomki/lexer.pyt   __init__?   s*    							c         C   s.   | d k r | d k p- | d k o- | d k S(   s\    Funkce ktera zjisti, jestli dany znak je pismeno. Pismeno je bud male, nebo velke pismeno. t   at   zt   At   Z(    (   R7   R9   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   isLetter]   s    c         C   s   | d k o | d k S(   sG    Funkce, ktera zjisti, jestli dany znak je cislice desitkove soustavy. t   0t   9(    (   R7   R9   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   isDigita   s    c         C   s1   | d k r' |  j  d 7_  d |  _ n  | d k S(   s1  
		Funkce, ktera zjisti, jestli dany znak je whitespace. Momentalne je
		whitespace mezera, tab a nebo novy radek. Opacna lomitka jsou ridici znaky,
		kterymi muzeme zapisovat specialni znaky, ktere nejsou na klavesnici.
		Takze 
 je konec radky, a ne opacne lomitko a male n. To by se napsalo jako \n.
		s   
i   t    s   	(   RA   s   	s   
(   R$   R%   (   R7   R9   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   isWhitespacee   s    c         C   s   | d k p | d k S(   sK    Funkce, která zjisti, jestli je daný znak číslice binární soustavy. R>   t   1(    (   R7   R9   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   isBinaryr   s    c         C   sF   | d k r | d k pE | d k r0 | d k pE | d k oE | d k S(   sQ    Funkce, která zjisti, jestli je daný znak číslice hexidecimální soustavy. R>   R?   R;   t   FR9   t   f(    (   R7   R9   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   isHexadecimalv   s    i    c         C   s5   |  j  t |  j � k  r* |  j |  j  | St j Sd S(   s-    Vrati aktualni token. Vysvetlime si priste. N(   R4   t   lenR"   R    t   _EOF(   R7   t   i(    (    s$   /home/tom/Development/Tomki/lexer.pyt   topTokenz   s    c         C   sc   |  j  �  } |  j t |  j � k  rR | d k s@ | | d k rR |  j d 7_ n |  j d � | S(   s.    Posune se na dalsi token. Vysvetlime priste. i    i   s   Očekáván jiný typ tokenuN(   RK   R4   RH   R"   t   Nonet   error(   R7   t   valuet   t(    (    s$   /home/tom/Development/Tomki/lexer.pyt   popToken�   s
    4c         C   s   |  j  t |  j � k S(   sJ    Vrati true, jestlize uz zadne dalsi tokeny nejsou. Vysvetlime si priste. (   R4   RH   R"   (   R7   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   isEOF�   s    i   c         C   s   |  j  |  j |  j | !S(   sq    Vrati aktualne zpracovavany znak. Tohle je funkce jen proto, abychom
		nemuseli porad psat ten slozity pristup. (   R5   R6   (   R7   RN   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   topChar�   s    c         C   s=   |  j  t |  j � k  r9 |  j  | 7_  |  j | 7_ n  d S(   s�   
		Posune nas na dalsi znak v aktualne analyzovanem retezci, pokud takovy
		existuje. Zase funkce pro prehlednost, abychom nemuseli mit to kontrolovani
		mezi vsude.
		N(   R6   RH   R5   R%   (   R7   RN   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   popChar�   s    c         C   s>   d t  |  j � d t  |  j � d | f GHt j d � d S(   sX    Funkce pro prehlednost, vypise ze doslo k chybe, k jake chybe doslo, a skonci program. s   Pri analyze doslo na radku s    cca v sloupci s    k chybe z duvodu: i   N(   t   strR$   R%   t   syst   exit(   R7   t   reason(    (    s$   /home/tom/Development/Tomki/lexer.pyRM   �   s    -c         C   s   |  j  j | | | f � d S(   s�   
		Funkce, ktera prida dany druh tokenu a pripadne i hodnotu na seznam jiz
		naparsovanych tokenu. Kdyz naparsujete nejaky token, musite zavolat tuhle
		funkci.
		N(   R"   t   append(   R7   t	   tokenTypet
   tokenValuet	   tokenLine(    (    s$   /home/tom/Development/Tomki/lexer.pyt   addToken�   s    c         C   s*   x# |  j  |  j �  � r% |  j �  q Wd S(   s7    Preskoci whitespace v aktualne zpracovavanem retezci. N(   RB   RR   RS   (   R7   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   skipWhitespace�   s    c         C   sj  d } |  j  |  j �  � s+ |  j d � n  xG |  j  |  j �  � rt | d t |  j �  � t d � } |  j �  q. W|  j �  d k rM|  j �  |  j  |  j �  � s� |  j d � n  t | � } d } | t |  j �  � t d � | } |  j �  xT |  j  |  j �  � rI| d } | t |  j �  � t d � | } |  j �  q� Wn  |  j t j | |  j	 � d S(	   s6    Naparsuje cislo v desitkove soustave a jeho hodnotu. i    s   Zacatek cisla musi byt cisloi
   R>   t   .s,   Po desetine tecce musi byt aspon jedno cislog      $@N(
   R@   RR   RM   t   ordRS   t   floatR\   R    t   NUMBERR$   (   R7   RN   t   x(    (    s$   /home/tom/Development/Tomki/lexer.pyt   parseNumber�   s&    $
$

$c         C   s�   d } |  j  |  j �  � s+ |  j d � n  xG |  j |  j �  � rt | d t |  j �  � t d � } |  j �  q. W|  j t j | |  j	 � d S(   s-    Naparsuje binární číslo a jeho hodnotu. i    s$   Zacatek cisla musi byt binarni cisloi   R>   N(
   RD   RR   RM   R@   R_   RS   R\   R    Ra   R$   (   R7   RN   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   parseBinaryNumber�   s    $c      	   C   s�  d } |  j  |  j �  � s+ |  j d � n  xA|  j  |  j �  � rn|  j �  } | d k r� | d k r� t | � t d � } n� | d k s� | d k r� d } n� | d k s� | d	 k r� d
 } n� | d k s� | d k r� d } np | d k s� | d k rd } nO | d k s| d k r%d } n. | d k s=| d k rFd } n |  j d � | d | } |  j �  q. W|  j t j | |  j � d S(   s3    Naparsuje hexadecimální číslo a jeho hodnotu. i    s*   Zacatek cisla musi byt hexadecimalni cisloR>   R?   R;   R9   i
   t   Bt   bi   t   Ct   ci   t   Dt   di   t   Et   ei   RE   RF   i   s-   Hexadecimalni cislo s nehexadecimalnimi znakyi   N(	   RG   RR   RM   R_   RS   R\   R    Ra   R$   (   R7   RN   Rb   t   y(    (    s$   /home/tom/Development/Tomki/lexer.pyt   parseHexadecimalNumber�   s.    						c         C   s�   |  j  } |  j |  j �  � s. |  j d � n  x8 |  j |  j �  � s[ |  j |  j �  � rh |  j �  q1 W|  j | |  j  !j �  } | |  j k r� |  j	 |  j | d |  j � n |  j	 t j | |  j � d S(   s)  
		Naparsuje identifikator nebo klicove slovo. Identifikator ma typ IDENT
		a svuj nazev jako hodnotu. Klicove slovo hodnotu nema, a typ ma podle toho,
		co je zac. Klicove slovo je takovy identifikator, ktery je ve slovniku
		klicovych slov, ktery jste inicializovali v metode __init__ nahore.
		s#   Identifikator musi zacinat pismenemN(   R6   R=   RR   RM   R@   RS   R5   t   lowerR#   R\   RL   R$   R    t   IDENT(   R7   RJ   RN   (    (    s$   /home/tom/Development/Tomki/lexer.pyt   parseIdentifierOrKeyword�   s    	- c         C   sR   | d |  _  d |  _ x5 |  j t |  j  � k  rM |  j d k rM |  j �  q Wd S(   s�    Rozkouskuje dany retezec na tokeny. Nastavi aktualne zpracovavany
		retezec na ten co funkci posleme, vynuluje aktualni pozici a vola funkci
		pro naparsovani tokenu dokuc neni cely retezec analyzovan. t    i    N(   R5   R6   RH   R&   t
   parseToken(   R7   t   string(    (    s$   /home/tom/Development/Tomki/lexer.pyt   analyzeString  s    	*c         C   s  |  j  �  |  j �  } |  j | � r2 |  j �  n�|  j | � rN |  j �  n�| d k r� |  j �  |  j t j	 d  |  j � n�| d k r� |  j �  |  j �  } | d k r� |  j �  |  j t j d  |  j � q|  j t j d  |  j � n$| d k r"|  j �  |  j t j d  |  j � n�| d k r�|  j �  |  j �  } | d k rv|  j �  |  j t j d  |  j � q|  j t j d  |  j � n�| d k re|  j �  |  j �  } | d k r�|  j �  |  j t j d  |  j � q| d k rI|  j �  x: |  j �  d k o(|  j |  j d d k s8|  j �  q�W|  j d � q|  j t j d  |  j � n�| d k r�|  j �  |  j t j d  |  j � n}| d	 k r�|  j �  |  j t j d  |  j � nK| d
 k r�|  j �  |  j t j d  |  j � n| d k r-|  j �  |  j t j d  |  j � n�| d k r_|  j �  |  j t j d  |  j � n�| d k r�|  j �  |  j �  } | d k r�|  j �  |  j t j d  |  j � q|  j t j d  |  j � nE| d k rn|  j �  |  j �  } | d k r#|  j �  |  j t j d  |  j � q| d k rR|  j |  j t j d  |  j � q|  j t j d  |  j � n�| d k r�|  j �  |  j t j d  |  j � nt| d k r�|  j �  |  j t j d  |  j � nB| d k r|  j �  |  j t j  d  |  j � n| d k r6|  j �  |  j t j! d  |  j � n�| d k rh|  j �  |  j t j" d  |  j � n�| d k r�|  j �  |  j t j# d  |  j � nz| d k r�|  j �  |  j t j$ d  |  j � nH| d k r�|  j �  |  j t j% d  |  j � n| d k r�|  j �  |  j �  d k r=|  j �  |  j& �  q|  j �  d k rf|  j �  |  j' �  q|  j �  d k r�|  j �  |  j �  q|  j( d � nu | d k r�|  j �  x\ |  j �  d k r�|  j �  q�Wn9 | d k r|  j t j) � d |  _* n |  j( d | � d  S(!   s�    Naparsuje jeden token ze vstupniho retezce. Preskoci whitespace a pak
		se rozhodne jestli se jedna o cislo, identifikator, klicove slovo, operator,
		atd. a overi ze je vse v poradku. Token prida do seznamu naparsovanych tokenu. R   R   R   R   R   i   i   R   t   &s   ||t   !R   R   R   R   R   R   R   R   R   R   R    t   $Rf   t   hRj   s   Neznamy typ cislat   #s   
Rr   s   Neznamy znak na vstupu! Znak: N(+   R]   RR   R=   Rq   R@   Rc   RS   R\   R    t   OP_ADDRL   R$   t   OP_EQUALt	   OP_ASSIGNt   OP_SUBSTRACTt	   OP_MOCNITt   OP_MULTIPLYt   OP_FLOORDIVISIONR5   R6   t	   OP_DIVIDER1   R2   R3   t   OP_REMAINDERt   OP_BIGGEROREQUALt	   OP_BIGGERt   OP_SMALLEROREQUALt   OP_NOTEQUALt
   OP_SMALLERt   OP_PARENTHESES_LEFTt   OP_PARENTHESES_RIGHTt   OP_BRACES_LEFTt   OP_BRACES_RIGHTt   OP_BRACKETS_RIGHTt   OP_BRACKETS_LEFTt   OP_COMMAt   OP_SEMICOLONRd   Rn   RM   RI   R&   (   R7   Rh   (    (    s$   /home/tom/Development/Tomki/lexer.pyRs     s�    









/





















N(?   t   __name__t
   __module__t   __doc__t   EOFRL   RI   Ra   Rp   R'   R(   R)   R*   R+   R,   R-   R.   R/   R0   R{   R|   R}   R~   R�   R�   R   R�   R�   R1   R2   R3   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R8   R=   R@   RB   RD   RG   RK   RP   RQ   RR   RS   RM   R\   R]   Rc   Rd   Rn   Rq   Ru   Rs   (    (    (    s$   /home/tom/Development/Tomki/lexer.pyR       sx   								
				
			(   RU   R    (    (    (    s$   /home/tom/Development/Tomki/lexer.pyt   <module>   s   � �