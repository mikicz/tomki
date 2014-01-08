ó
ÚïËRc           @   s1   d  d l  Td  d l m Z d d d     YZ d S(   iÿÿÿÿ(   t   *(   t   Lexert   Parserc           B   sÑ   e  Z d  Z d   Z d d  Z d d  Z d   Z d   Z d   Z	 d   Z
 d	   Z d
   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z d   Z RS(   sv  
	Ten parser se trosku lisi od toho parseru, ktery jsme delali na hodine, protoze uz pouziva ty jednoduzsi stromy, o kterych jsem mluvil. Takze misto toho, aby kazde pravidlo melo svoji vlasti tridu (v ast), tak ty tridy pro ten strom odpovidaji spis tomu, co ten program bude delat, nez tomu, jak je napsana gramatika. Blizsi popisky viz jednotlive parsovaci metody nize.
	c         C   s   | |  _  d S(   s?    Zalozi parser a zapamatuje si lexer, se kterym bude pracovat. N(   t   lexer(   t   selfR   (    (    s'   /home/tom/Development/Tomki/slparser.pyt   __init__   s    	c         C   so   | d k r |  j j   S|  j j   } | d | k rE |  j j   St d | d t | d  d   d S(   sº    Abych nemusel tolik psat, provede pop z lexeru. Kdyz specifikuju druh tokenu, ktery ocekavam, tak zaroven zkontroluje jestli je to spravny typ, a vyhodi vyjimku, kdyz tomu tak neni. 
		i    s   Ocekavany token s    neni na vstupu (s    misto nej)N(   t   NoneR   t   popTokent   topTokent   SyntaxErrort   str(   R   t   typet   t(    (    s'   /home/tom/Development/Tomki/slparser.pyt   pop   s    i    c         C   s   |  j  j |  S(   sV    Abych nemusel tolik psat, provede top() z lexeru. 
		MÅ¯Å¾e se zeptat na token + i
		(   R   R   (   R   t   i(    (    s'   /home/tom/Development/Tomki/slparser.pyt   top   s    c         C   sJ   t    } x: |  j   d t j k rE | j |  j    |  j   q W| S(   s   Hlavni metoda na parsovani, odpovida pravidlu pro program:

		PROGRAM ::= { STATEMENT }

		Z hlediska stromu (ast) je program tedy blok prikazu, postupne jak prikazy parsuju tak je pridavam do toho bloku. Kdyz zjistim, ze uz na vstupu zadny token nemam, tak jsem skoncil.
		i    (   t   BlockR   R   t   EOFt   addt   parseStatementR   (   R   t   program(    (    s'   /home/tom/Development/Tomki/slparser.pyt   parse"   s
    	c         C   s½   |  j    d t j k r# |  j   S|  j    d t j k rF |  j   S|  j    d t j k ri |  j   S|  j    d t j k r |  j	   S|  j    d t j
 k r¯ |  j   S|  j   Sd S(   sa    STATEMENT ::= ( CONDITION | LOOP | E | FDEF ) ;

		Statement je bud if, nebo zapis promenne. 
		i    N(   R   R   t   KW_IFt   parseIfStatementt   KW_WHILEt
   parseWhilet   KW_FORt   parseFort   KW_FUNCTIONt   parseFunctiont   OP_BRACES_LEFTt
   parseBlockt   parseAssignment(   R   (    (    s'   /home/tom/Development/Tomki/slparser.pyR   /   s    




c         C   s?   |  j  t j  d } |  j  t j  |  j   } t | |  S(   s8   ASSIGNMENT ::= ident op_assign EXPRESSION
	   
		Ulozeni hodnoty do promenne vypada tak, ze na leve strane je identifikator promenne, hned za nim je operator prirazeni a za nim je vyraz, ktery vypocitava hodnotu, kterou do promenne chci ulozit. Tohle je zjednodusena verze prirazeni, viz komentare k hodine. 
		i   (   R   R   t   IDENTt	   OP_ASSIGNt   parseExpressiont   VariableWrite(   R   t   variableNamet   rhs(    (    s'   /home/tom/Development/Tomki/slparser.pyR    A   s    c         C   s_   |  j    } xL |  j   d t j k rZ |  j   d |  j    } t | | t j  } q W| S(   s    E0 ::= E1 { OP_OR E1 } i    (   t   parseE1R   R   t   OP_ORR   t   BinaryOperator(   R   t   lhsR&   (    (    s'   /home/tom/Development/Tomki/slparser.pyR#   K   s    c         C   s_   |  j    } xL |  j   d t j k rZ |  j   d |  j    } t | | t j  } q W| S(   s    E1 ::= E2 { OP_AND E2 } i    (   t   parseE2R   R   t   OP_ANDR   R)   (   R   R*   R&   (    (    s'   /home/tom/Development/Tomki/slparser.pyR'   T   s    c         C   sg   |  j    } xT |  j   d t j t j f k rb |  j   d } |  j    } t | | |  } q W| S(   s-    E2 ::= E3 { ( OP_EQUAL | OP_NOTEQUAL ) E3 } i    (   t   parseE3R   R   t   OP_EQUALt   OP_NOTEQUALR   R)   (   R   R*   t   opR&   (    (    s'   /home/tom/Development/Tomki/slparser.pyR+   ]   s    %c         C   ss   |  j    } x` |  j   d t j t j t j t j f k rn |  j   d } |  j    } t | | |  } q W| S(   sT    E3 ::= E4 { ( OP_BIGGER | OP_SMALLER | OP_BIGGEROREQUAL | OP_SMALLEROREQUAL ) E4 } i    (	   t   parseE4R   R   t	   OP_BIGGERt
   OP_SMALLERt   OP_BIGGEROREQUALt   OP_SMALLEROREQUALR   R)   (   R   R*   R0   R&   (    (    s'   /home/tom/Development/Tomki/slparser.pyR-   f   s    1c         C   sg   |  j    } xT |  j   d t j t j f k rb |  j   d } |  j    } t | | |  } q W| S(   s,    E4 ::= E5 { ( OP_ADD | OP_SUBSTRACT ) E5 } i    (   t   parseE5R   R   t   OP_ADDt   OP_SUBSTRACTR   R)   (   R   R*   R0   R&   (    (    s'   /home/tom/Development/Tomki/slparser.pyR1   o   s    %c         C   sy   |  j    } xf |  j   d t j t j t j t j t j f k rt |  j   d } |  j    } t	 | | |  } q W| S(   s\    E5 ::= E6 { ( OP_MULTIPLY | OP_MOCNIT | OP_DIVIDE | OP_FLOORDIVISION | OP_REMAINDER ) E6 } i    (
   t   parseE6R   R   t   OP_MULTIPLYt	   OP_MOCNITt	   OP_DIVIDEt   OP_FLOORDIVISIONt   OP_REMAINDERR   R)   (   R   R*   R0   R&   (    (    s'   /home/tom/Development/Tomki/slparser.pyR6   x   s    7c         C   sj   |  j    d t j k rZ |  j t j  d |  j   } t t d d f | t j  } n |  j   } | S(   s    E6 ::= [ OP_SUBSTRACT ] F i    N(   R   R   R8   R   t   parseFR)   t   numberR   (   R   R&   R*   (    (    s'   /home/tom/Development/Tomki/slparser.pyR9      s    !c         C   sJ  |  j    d t j k r3 |  j   d } t |  S|  j    d t j k r |  j  d  d t j k r |  j   d } t |  S|  j    d t j k rº |  j  d  d t j k rº n |  j    d t j k rö |  j  d  d t j k rö |  j	 S|  j    d t j k rt
   S|  j t j  |  j   } |  j t j  | Sd S(   s   F ::= number | ident [ OP_BRACKETS_LEFT E OP_BRACKETS_RIGHT ] | FCALL | OP_PARENTHESES_LEFT E OP_PARENTHESES_RIGHT| FIELD
		
		Faktorem vyrazu pak je bud cislo (literal), nebo nazev promenne, v tomto pripade se vzdycky jedna o cteni promenne a nebo znova cely vyraz v zavorkach. 
		i    i   N(   R   R   t   NUMBERR   t   LiteralR!   t   OP_BRACKETS_LEFTt   VariableReadt   OP_PARENTHESES_LEFTt   parseFunctionCallt
   parseArrayR#   t   OP_PARENTHESES_RIGHT(   R   t   valueR%   t   result(    (    s'   /home/tom/Development/Tomki/slparser.pyR?      s     
5
55c         C   s  |  j  t j  |  j  t j  |  j   } |  j  t j  |  j   } g  } xr |  j   d t j k rÂ |  j    |  j  t j  |  j   } |  j  t j  |  j   } | j	 | | g  qQ W|  j   d t j
 k rõ |  j    |  j   } n	 t   } t | | | |  S(   sÀ    
		CONDITION ::= KW_IF '(' E ')' BLOCK { KW_ELIF '(' E ')' BLOCK } [ KW_ELSE BLOCK ]
	
		If podminka je klasicky podminka a za ni block, nekoneÄnÃ½ poÄet elifÅ¯, pak pripadne else block.
		i    (   R   R   R   RE   R#   RH   R   R   t   KW_ELIFt   appendt   KW_ELSER   t   If(   R   t	   conditiont   trueCaset   elifst   xt   yt	   falseCase(    (    s'   /home/tom/Development/Tomki/slparser.pyR   ¨   s$    

	c         C   sU   |  j  t j  |  j  t j  |  j   } |  j  t j  |  j   } t | |  S(   s   
		KW_WHILE '(' E ')' BLOCK
		(   R   R   R   RE   R#   RH   R   t   While(   R   RO   t   block(    (    s'   /home/tom/Development/Tomki/slparser.pyR   Æ   s    c         C   sì   |  j  t j  |  j   } |  j  t j  |  j   d t j k rp |  j d  d t j k rp |  j   } n` |  j   d t j k r¨ t	 |  j  t j  d  } n( |  j   d t j
 k rÐ |  j   } n  |  j   } t | | |  S(   s7   
		KW_FOR ident KW_IN ( ident | FCALL | FIELD) BLOCK
		i    i   (   R   R   R   R?   t   KW_InR   R!   RE   RF   RD   RC   RG   R   t   For(   R   t   vart   arrayRV   (    (    s'   /home/tom/Development/Tomki/slparser.pyR   Ó   s    5c         C   s`   |  j  t j  t   } x0 |  j   d t j k rK | j |  j    q W|  j  t j  | S(   su    BLOCK ::= op_braceopen { STATEMENT } op_braceclose

		Blok je podobny programu, proste nekolik prikazu za sebou. 
		i    (   R   R   R   R   R   t   OP_BRACES_RIGHTR   R   (   R   RJ   (    (    s'   /home/tom/Development/Tomki/slparser.pyR   ä   s    	c         C   s¤   |  j  t j  } |  j  t j  g  } x\ |  j   d t j k r | j |  j    |  j   d t j k r+ |  j  t j  q+ q+ W|  j  t j  t	 | |  S(   s?    FCALL ::= ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT i    (
   R   R   R!   RE   R   RH   RL   R#   t   OP_COMMAt   FunctionCall(   R   t   functionNamet   arrgs(    (    s'   /home/tom/Development/Tomki/slparser.pyRF   ð   s    c         C   s½   |  j  t j  } |  j  t  g  } xl |  j   d t j k r | j t |  j  t j  d   |  j   d t j k r( |  j  t j  q( q( W|  j  t  |  j	   } t
 | | |  S(   sP    FDEF :== KW_FUNCTION ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT BLOCK i    i   (   R   R   R!   RE   R   RL   t	   ArrgIdentR\   RH   R   t   FunctionWrite(   R   R^   R_   RV   (    (    s'   /home/tom/Development/Tomki/slparser.pyR   ü   s    #c         C   sm   |  j  t  g  } x@ |  j   d t j k rU | j |  j    |  j  t j  q W|  j  t  t |  S(   Ni    (	   R   RC   R   R   t   OP_BRACKETS_RIGHTRL   R#   R\   t   Array(   R   t   polozkypole(    (    s'   /home/tom/Development/Tomki/slparser.pyRG   
  s    N(   t   __name__t
   __module__t   __doc__R   R   R   R   R   R   R    R#   R'   R+   R-   R1   R6   R9   R?   R   R   R   R   RF   R   RG   (    (    (    s'   /home/tom/Development/Tomki/slparser.pyR      s,   				
													
							N(    (   t   astR   R   R   (    (    (    s'   /home/tom/Development/Tomki/slparser.pyt   <module>   s   
