# -*- coding: utf-8 -*-
"""
Made by: Sara Martin (NIU: 1669812) and Lara Rodriguez (NIU: 1667906)
"""
"""
SYNTACTIC TREE FUNCTIONS
"""
def IsLowerLetter(char):
    return ("a"<=char<="z")
def IsNumber(char):
    return ("0"<=char<="9")
def IsNegation(char):
    return (char=="¬")
def IsOpeningBracket(char):
    return (char=="(")
def IsClosingBracket(char):
    return (char==")")
def IsConnector(char):
    return (char=="|" or char=="&" or char=="-" or char=="+")
def IsNullOrEmpty(string):
    return (string==None) or (len(string)==0)
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
TRUTH TABLE FUNCTIONS
"""
def FillDictionary(dict1,expression,subExpressions):
    if IsAtomicSentence(expression):
        return dict1
    else:
        #Append subexpressions to key expression
        dict1.setdefault(expression, [])
        for subexpression in subExpressions:
            dict1[expression].append(subexpression)
        #Append main connector to key expression
        if expression[0]=="¬":
            connector="¬"
        else:
            expression_2=RemoveOuterBrackets(expression)
            position_connector=PositionMainConnector(expression_2)
            if position_connector==None:
                connector="¬"
            else:
                connector=expression_2[position_connector]
        dict1[expression].append(connector)
        return dict1

"""
MAIN
"""    
print("Welcome! This program computes truth table of any logic sentence.\n"
     "Please, use the following symbols as connectors: ¬ as negation, -> as conditional, "
     "|| as disjunction, <-> as biconditional and && as conjuction.\n")

#Make syntacticTree
string=input("Enter the logic sentence: ")
string = PreProcessingData(string)
numberAtomicSentences = NumberAtomicSentences(string)
syntacticTree = []
for i in range(numberAtomicSentences):
    syntacticTree.append([string])
dict1={}
level = 1
badExpression = False
while badExpression==False:
    expressions = GetFormulasLastLevel(level- 1)
    if (IsFinished(syntacticTree)):
        finalMessage = "The sentence is a Propositional Logic Formula"
        Do_truth_table=True 
        break
    level+=1
    for i in range(len(expressions)):
        subExpressions = SubExpressions (expressions[i])
        if subExpressions==None: 
            badExpression=True
            print("The expression "+str(expressions[i])+" is not a Formula in Propositional Logics.\nThe truth-table was aborted.")
            Do_truth_table=False
            break
        dict1=FillDictionary(dict1,expressions[i],subExpressions)
        for j in range(len(subExpressions)):
            syntacticTree=FillSyntancticTree(syntacticTree,subExpressions[j],level)

if Do_truth_table==True:

    #Get header of Truth table
    header=[]
    for i in range(len(syntacticTree[0])-1,-1,-1):
        for nested in syntacticTree:
            if nested[i] not in header:
                header.append(nested[i])
                
    #Get number of atomic sentences in header
    nAtomicSentences=0
    for formula in header:
        if IsAtomicSentence(formula):
            nAtomicSentences+=1

    #Create empty list of Truth values
    Truth_table=[]
    for i in range(2**nAtomicSentences):
        Truth_table.append([])

    #Fill the truth-values of the atomic sentences
    import itertools
    Truth_table = list(itertools.product([True,False],repeat=nAtomicSentences))
    import numpy as n
    Truth_table = n.array(Truth_table) 
    Truth_table = Truth_table.tolist()

    #Get dictionary with positions of formulas in header
    header_positions={}
    index=0
    for formula in header:
        header_positions[formula]=index
        index+=1

    #Fill the truth-values of the other formulas
    for formula in header[nAtomicSentences:]:
        sublist=dict1[formula] #[subformula1, subformula2, connector]
        for i in range(len(Truth_table)):
            value1=Truth_table[i][header_positions[sublist[0]]]
            if len(sublist)==2:
                Truth_table[i].append(not value1)
            else:
                value2=Truth_table[i][header_positions[sublist[1]]]
                connector = sublist[2]
                if connector == "&":
                    Truth_table[i].append(value1 and value2)
                elif connector == "|":
                    Truth_table[i].append(value1 or value2)
                elif connector == "-":
                    Truth_table[i].append((not value1) or (value1 and value2))
                elif connector == "+":
                    Truth_table[i].append((value1 and value2) or ((not value1) and (not value2)))

    #Print result
    print(header)
    n=""
    for row in Truth_table:
        for i in range(len(row)):
            n += str(row[i])
            if i < len(row)-1:
                n += ";"
        n += "\n"
    print(n)
    c = 0
    for row in Truth_table:
        if row[-1]== True:
            c+=1
    if c == 0:
        print("The logic sentence is a contradiction")
    elif c == 2**nAtomicSentences:
        print("The logic sentece is a tautology")
    else:
        print("The logic sentence is a contingency")
    



        
        
        

