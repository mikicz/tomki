# -*- coding: utf-8 -*-
from Frame import Frame
from Literal import Literal

class FunctionCall:
    """
    AST pro volání funkce, pamatuje si jméno funkce a argumenty, které poté dosadí do volání.
    """

    def __init__(self, name, arguments):
        
        self.name = name
        self.arguments = arguments # pole argumentů
        self.type = "FunctionCall"

    def __str__(self): # pro jednoduché printování
        
        if (self.arguments == []): # pokud je volání bez argumentů
            return " %s ()" % (self.name,)
        
        else:
            result = "%s ("  % (self.name,)
            firstArgument = True
            
            for y in self.arguments:
                if (firstArgument): # první argument před sebou nemá čárku
                    result += y.__str__() # přidá se __str__ podřazeného AST
                    firstArgument = False
                else:
                    result += ", "+ y.__str__()
                
            
            result += ") "
            return result

    def run (self, frame, functionFrame): # samotné spuštění funkce 
        (argumentNames, block) = functionFrame.get(self.name) # vytáhnu si z functionFrame jména argumentů a blok, který se má spouštět
        newFrame = Frame(frame) # nový Frame, ve kterém se funkce spustí, s odkazem na mateřský frame pro globální proměné
        for i in range(0, len(argumentNames)):
            newFrame.set(argumentNames[i], self.arguments[i].run(frame,functionFrame), functionFrame) # přidám do newFrame všechny proměné se správnými jmény
       
        try:
            block.run(newFrame, functionFrame) # pustí block příkazů přiřazený k funkci
        except Literal, e: # Literal je používán k odchycení returnu
            return e
        