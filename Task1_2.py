# -*- coding: utf-8 -*-

"""
This program computes a syntactic tree of any logic sentence.
Made by: Sara Martin (NIU: 1669812) and Lara Rodriguez (NIU: 1667906)
"""

"""
BASIC FUNCTIONS
"""
def IsLowerLetter(char):
    return ("a"<=char<="z")
def IsNumber(char):
    return ("0"<=char<="9")
def IsNegation(char):
    return (char=="¬")
def IsOpeningBracket(char):
    return (char=="(" or char=="[")
def IsClosingBracket(char):
    return (char==")" or char=="]")
def IsConnector(char):
    return (char=="|" or char=="&" or char=="-" or char=="+")
def IsNullOrEmpty(string):
    return (string==None) or (len(string)==0)

"""
I/O FUNCTIONS
"""
def PreProcessingData(string):
    return string.replace(" ","").replace("<->","+").replace("->","-").replace("||", "|").replace("&&", "&")
    
def OutputData(expression):
    return expression.replace("+", "<->").replace("-", "->").replace("|", "||").replace("&", "&&")

def PrintResult(syntacticTree,finalMessage): 
    for row in range(len(syntacticTree)):
        for level in range(len(syntacticTree[i])):
            if syntacticTree[row][level]==None:
                syntacticTree[row][level]=""
        row="  ".join(syntacticTree[row])
        print(row)
    if finalMessage==None:
        print("BAD FORMAT")
    else:
        print(finalMessage)

"""
ATOMIC SENTENCE FUNCTIONS
"""
def IsAtomicSentence(expression):
    numberOfLoweLetters = 0
    badCharacters = 0
    for i in range(len(expression)):
        char = expression[i]
        if IsLowerLetter(char)==False or IsNumber(char)==True:
            badCharacters+=1
        elif IsLowerLetter(char)==True:
            numberOfLoweLetters += 1    
    f = IsLowerLetter(expression[0]) 
    m = numberOfLoweLetters > 1 
    b = badCharacters > 0  
    return (f==True and m==False and b==False)
    
def NumberAtomicSentences(expression):
    numberAtomicSenteces = 0
    i=0
    while i<len(expression):
        char = expression[i]
        if IsLowerLetter(char)==True:
            numberAtomicSenteces += 1
        i+=1
    return numberAtomicSenteces

"""
BRACKET FUNCTIONS
"""
def RemoveOuterBrackets(expression):
    if (IsOpeningBracket(expression[0]) and IsClosingBracket(expression[-1])):
        expression=expression[1:-1]
        if (ImpairBrackets(expression)):
            expression="("+expression+")"
    return expression
    
def ImpairBrackets(expression):
    numberOfBrackets=0
    for char in expression:
        if IsOpeningBracket(char):
            numberOfBrackets+=1
        elif IsClosingBracket(char):
            numberOfBrackets-=1
        if numberOfBrackets<0:
            return True
    if numberOfBrackets!=0:
        return True
    else:
        return False
        
def NoBracketsAndDiffConnectors(expression):
    connectors=[]
    for char in expression:
        if (IsOpeningBracket(char) or IsClosingBracket(char)):
            return False
        elif IsConnector(char):
            if char not in connectors:
                connectors.append(char)
    if len(connectors)==1:
        return False
    else:
        return True

def DifferentBrackets(expression):
    if expression[0]=="(":
        if expression[-1]!=")":
            return True
        else:
            return False
    elif expression[0]=="[":
        if expression[-1]!="]":
            return True
        else:
            return False

"""
FORMULAS ANALYSIS FUNCTIONS
"""
def GetFormulasLastLevel(level):
    expressions=[]
    for i in range(len(syntacticTree)):
        if (syntacticTree[i][level] not in expressions) or (IsAtomicSentence(syntacticTree[i][level])):
            expressions.append(syntacticTree[i][level])
    return expressions    
    
def SubExpressions(expression):
    if IsNullOrEmpty(expression):
        return None 
    elif IsAtomicSentence(expression):
        return [expression]
    elif expression[0]=="¬":
        return [expression[1:]]
    elif (IsOpeningBracket(expression[0]) and IsClosingBracket(expression[-1])):
        if DifferentBrackets(expression):
            return None
    expression=RemoveOuterBrackets(expression)
    if NoBracketsAndDiffConnectors(expression):
        return None
    positionMainConnector = PositionMainConnector(expression)
    if positionMainConnector== None: 
        return None
    leftExpression= expression[:positionMainConnector] 
    rightExpression= expression[positionMainConnector+ 1:]
    if (IsNullOrEmpty(leftExpression)==True) or (IsNullOrEmpty(rightExpression)==True):
        return None
    elif (NumberAtomicSentences(leftExpression) <= 0) or (NumberAtomicSentences(rightExpression) <= 0):
        return None
    subExpressions=[leftExpression,rightExpression]               
    return subExpressions
        
def PositionMainConnector(expression):
    positionMainConnector=None
    numberOfBrackets=0
    for i in range(len(expression)):
        char=expression[i]
        if IsOpeningBracket(char)==True:
            numberOfBrackets += 1
        elif IsClosingBracket(char)==True:
            numberOfBrackets -= 1
        elif (IsConnector(char)==True) and (numberOfBrackets == 0):
            positionMainConnector = i
            break
    return positionMainConnector

"""
SYNTACTIC TREE
"""
def IsFinished(syntacticTree): 
    lastLevel = len(syntacticTree[0]) -1
    for i in range(len(syntacticTree)):
        expression = syntacticTree[i][lastLevel]
        if (expression==None) or (IsAtomicSentence(expression)==False):
            return False
    return True
    
def FillSyntancticTree(syntacticTree,expression,level):
    if level > len(syntacticTree[0]):
        for i in range(len(syntacticTree)):
            syntacticTree[i].append(None)
    numberOfAtomicSentences = NumberAtomicSentences(expression)
    i=0
    count=0
    while (i<len(syntacticTree)) and (count < numberOfAtomicSentences):
        if syntacticTree[i][level-1]==None:
            syntacticTree[i][level-1]=expression
            count+=1
        i+=1
    return syntacticTree    

"""
MAIN
"""    
print("Welcome! This program computes a syntactic tree of any logic sentence. "
     "Please, use the following symbols as connectors: ¬ as negation, -> as conditional, "
     "|| as disjunction, <-> as biconditional and && as conjuction.\n ")

string=input("\nEnter the logic sentence: ")
string = PreProcessingData(string)
numberAtomicSentences = NumberAtomicSentences(string)
syntacticTree = []
for i in range(numberAtomicSentences):
    syntacticTree.append([string])
level = 1
badExpression = False
while badExpression==False:
    expressions = GetFormulasLastLevel(level- 1)
    if (IsFinished(syntacticTree)): 
        finalMessage = "The sentence is a Propositional Logic Formula"
        break
    level+=1
    for i in range(len(expressions)):
        subExpressions = SubExpressions (expressions[i])
        if subExpressions==None: 
            badExpression=True
            finalMessage=("The expression "+str(expressions[i])+" is not a Formula in Propositional Logics.\nThe Syntactic Tree was aborted.")
            break
        for j in range(len(subExpressions)):
            syntacticTree=FillSyntancticTree(syntacticTree,subExpressions[j],level)
connectors_string = []
for elements in string:
    if elements in "-+|&¬":
        connectors_string.append(elements)
conj = []
dis= []
for ele in connectors_string:
    if ele == "&":
        conj.append(ele)
    if ele == "|":
        dis.append(ele)
if len(conj) == len(connectors_string):
    syta = []
    for rows in syntacticTree:
        syntac = []
        syta.append(syntac)
        syntac.append(rows[0])
        syntac.append(rows[-1])
    PrintResult(syta, finalMessage)
elif len(dis) == len(connectors_string):
    syta = []
    for rows in syntacticTree:
        syntac = []
        syta.append(syntac)
        syntac.append(rows[0])
        syntac.append(rows[-1])
    PrintResult(syta, finalMessage)
else:
    PrintResult(syntacticTree,finalMessage)