#gramatika

    IDENTIFIKATOR ::= a..z|A..Z{0..0|a..z|A..Z}		# Identifikátory začínají písmenem a mají v sobě písmena či čísla
    CISLO ::= ["$d"]0..9{0..9}[.0..9{0..9}]
    BINARNICISLO ::= "$b" 0|1{0|1}					# binární a hex čísla pouze s $b nebo $h (decimální mají $d)
    HEXADECIMALNICISLO ::= "$h" 0..9|A..F{0..9|A..F}
    OPERATOR ::= +|-|/|*|^|&|!|"|"|and|or|not|==|!=|%|**|//|<>|>|<|>=|<=|&|"||"|!
    RIDICIZNAKY ::= "("|")"|"{"|"}"|"["|"]"			# prakticky totéž co operátory
    KEYWORD ::= if|else|elif|while|for|break|continue|return|function|in

##podminky

    PROGRAM ::= { STATEMENT }
    
    STATEMENT ::= ( CONDITION | LOOP | E | FDEF | BLOCK ) ;
    
    BLOCK ::= OP_BRACES_LEFT { STATEMENT } OP_BRACES_RIGHT
    
    CONDITION ::= KW_IF '(' E ')' BLOCK { KW_ELIF '(' E ')' BLOCK } [ KW_ELSE BLOCK ]
    
    LOOP ::= KW_WHILE '(' E ')' BLOCK | KW_FOR ident KW_IN ( ident | FCALL | ARRAY) BLOCK
    
    
    FDEF :== KW_FUNCTION ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT BLOCK
    
    E ::= E1 [ OP_ASSIGN E1 ] #aka ASSIGNMENT ::= ident op_assign EXPRESSION
    E1 ::= E2 { OP_OR E1 }
    E2 ::= E3 { OP_AND E2 }
    E3 ::= E4 { ( OP_EQUAL | OP_NOTEQUAL ) E3 }
    E4 ::= E5 { ( OP_BIGGER | OP_SMALLER | OP_BIGGEROREQUAL | OP_SMALLEROREQUAL ) E4 }
    E5 ::= E6 { ( OP_ADD | OP_SUBSTRACT ) E5 }
    E6 ::= E7 { ( OP_MULTIPLY | OP_MOCNIT | OP_FLOORDIVISION | OP_REMAINDER ) E6 }
    E7 ::= [ OP_SUBSTRACT ] F
    F ::= number | ident [ OP_BRACKETS_LEFT [ E ]{, E } OP_BRACKETS_RIGHT ] | FCALL | OP_PARENTHESES_LEFT E OP_PARENTHESES_RIGHT| ARRAY | STRING
    
    STRING ::== """ fuckingeverything """ | "'" fucking everything "'"
    
    ARRAY ::= OP_BRACKETS_LEFT E { ,E } OP_BRACKETS_RIGHT # definice pole (např. když píšu "x = [2, 4]")
    
    FCALL ::= ident OP_PARENTHESES_LEFT ARGS OP_PARENTHESES_RIGHT
    
    ARGS ::= [ E { OP_COMMA E } ]