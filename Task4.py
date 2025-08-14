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
def MakeSyntacticTree(string, syntacticTree):
    string = PreProcessingData(string)
    numberAtomicSentences = NumberAtomicSentences(string)
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
                finalMessage = "The expression "+str(expressions[i])+" is not a Formula in Propositional Logics.\nThe truth-table was aborted."
                Do_truth_table=False
                break
            dict1=FillDictionary(dict1,expressions[i],subExpressions)
            for j in range(len(subExpressions)):
                syntacticTree=FillSyntancticTree(syntacticTree,subExpressions[j],level)
    return syntacticTree, finalMessage, Do_truth_table, dict1

def MakeHeader(syntacticTree):
    header=[]
    for i in range(len(syntacticTree[0])-1,-1,-1):
        for nested in syntacticTree:
            if nested[i] not in header:
                header.append(nested[i])
    return header
def MakeCombinedHeader(syntacticTrees):
    header=[]
    for syntacticTree in syntacticTrees:
        for i in range(len(syntacticTree[0])-1,-1,-1):
            for nested in syntacticTree:
                if nested[i] not in header:
                    header.append(nested[i])
    header = sorted(header, key = lambda sub : len(list(set(sub))))
    return header
def MakeTruthTable(dictionaryy, header):
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
        sublist=dictionaryy[formula] #[subformula1, subformula2, connector]
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
    return Truth_table, nAtomicSentences

"""
MAIN
"""
def menu():
    print("\nCHOOSE AN OPTION\n"
    "(1) Tautology\n"
    "(2) Contradiction\n"
    "(3) Logical Equivalence\n"
    "(4) Satisfiability\n"
    "(5) Logical Consequence\n")

menu()
options=["1","2","3","4","5"]
option=input()

while option not in options:
    option=input("Please choose one of the options available: ")

if option == "1":
    syntacticTree=[]
    Tautology=True
    string=input("Enter logic sentence: ")
    syntacticTree, finalMessage, Do_truth_table, dict1 = MakeSyntacticTree(string,syntacticTree)
    if not Do_truth_table:
        print("That sentence is not correct.")
    else:
        header=MakeHeader(syntacticTree)
        Truth_table, nAtomicSentences = MakeTruthTable(dict1, header)
        for i in range(len(Truth_table)): #i=row
            if Truth_table[i][-1]==False:
                Tautology=False
                print("The sentence is not a Tautology.\nYou can find the next counter-example: ")
                for j in range(nAtomicSentences):
                    print(str(header[j])+"="+str(Truth_table[i][j]))
                break
        if Tautology==True:
            print("The sentence is a Tautology.")
    print("FINISHED") 

elif option == "2":
    syntacticTree=[]
    Contradiction=True
    string=input("Enter logic sentence: ")
    syntacticTree, finalMessage, Do_truth_table, dict1 = MakeSyntacticTree(string,syntacticTree)
    if not Do_truth_table:
        string=input("That sentence is not correct.")
    else:
        header=MakeHeader(syntacticTree)
        Truth_table, nAtomicSentences = MakeTruthTable(dict1, header)
        for i in range(len(Truth_table)): #i=row
            if Truth_table[i][-1]==True:
                Contradiction=False
                print("The sentence is not a Contradiction.\nYou can find the next counter-example: ")
                for j in range(nAtomicSentences):
                    print(str(header[j])+"="+str(Truth_table[i][j]))
                break
        if Contradiction==True:
            print("The sentence is a Contradiction.")
    print("FINISHED")

elif option == "3":
    Equivalence=True
    string_1 = input("Enter first sentence: ")
    string_2 = input("Enter second sentence: ")
    syntacticTree=[]
    #Make syntacticTree of string 1
    syntacticTree_1, finalMessage, Do_truth_table_1, dict1_1 = MakeSyntacticTree(string_1,syntacticTree)
    if not Do_truth_table_1:
        print("Sentence 1 is not correct.")
    #Make syntacticTree of string 2
    syntacticTree=[]
    syntacticTree_2, finalMessage, Do_truth_table_2, dict1_2 = MakeSyntacticTree(string_2,syntacticTree)
    if not Do_truth_table_2:
        string=input("Sentence 2 is not correct.")
    else:
        #Make both Truth tables
        header_1 = MakeHeader(syntacticTree_1)
        header_2 = MakeHeader(syntacticTree_2)
        Truth_table_1, nAtomicSentences_1 = MakeTruthTable(dict1_1, header_1)
        Truth_table_2, nAtomicSentences_2 = MakeTruthTable(dict1_2, header_2)
        for i in range(len(Truth_table_1)):
            if Truth_table_1[i][-1]!=Truth_table_2[i][-1]:
                Equivalence = False
                print("Sentence "+string_1+" and sentence "+string_2+" are not logically equivalent.\nYou can find the next counter-example: ")
                for j in range(nAtomicSentences_1):
                    print(str(header_1[j])+"="+str(Truth_table_1[i][j]))
                for z in range(nAtomicSentences_2):
                    print(str(header_2[z])+"="+str(Truth_table_2[i][z]))
                break
        if Equivalence==True:
            print("The sentences are equivalent.")
    print("FINISHED")

elif option == "4":
    #Ask for the number of sentences
    correct=False
    while correct==False:
        try:
            num = int(input("How many sentences are you including in your analysis: "))
        except:
            print("Number must be an integer.")
        else:
            if num>=2:
                correct=True
            else:
                print("Number of sentences must be greater than 1.")
    #Ask for the sentences and append them in a list
    sentences = []
    for i in range(num):
        sentence = input("Write the sentence "+str(i+1)+": ")
        sentences.append(sentence)
    #For each sentence, make its syntactic Tree and dictionary and store them in lists
    syntacticTrees=[]
    dicts=[]
    for sentence in sentences:
        syntacticTree=[]
        syntacticTree, finalMessage, Do_truth_table, dict1 = MakeSyntacticTree(sentence,syntacticTree)
        if Do_truth_table==False:
            print("Sentence "+str(sentence)+" is a bad Propositional logic sentence. Process was aborted.")
            break
        syntacticTrees.append(syntacticTree)
        dicts.append(dict1)
    #Create an unified dictionary combining all dictionaries from all sentences
    new_dict = {}
    for dictionary in dicts:
        new_dict.update(dictionary)
    #Get the truth_table
    header = MakeCombinedHeader(syntacticTrees)
    Truth_table, nAtomicSentences = MakeTruthTable(new_dict, header)
    #Check if there is a valuation that makes all sentences True
    Satisfiable = False
    for row in Truth_table:
        values = row[-num:]
        if all(value == True for value in values):
            Satisfiable = True
            break
    if Satisfiable == True:
        print("The sentences are satisfiable. You can find the next example: ")
        for i in range(nAtomicSentences):
            print(str(header[i])+ "="+str(row[i]))
    else:
        print("The sentences are not satisfiable.")
    print("FINISHED")
            
elif option == "5":
    #Ask for the number of sentences
    correct=False
    while correct==False:
        try:
            num = int(input("How many premises are you including in your analysis: "))
        except:
            print("Number must be an integer.")
        else:
            if num>=1:
                correct=True
            else:
                print("Number of sentences must be greater than 1.")
    #Ask for the premises and append them in a list
    sentences = []
    for i in range(num):
        sentence = input("Write premise "+str(i+1)+": ")
        sentences.append(sentence)
    #Ask for conclusion and append it too
    sentence = input("Write the conclusion: ")
    sentences.append(sentence)
    #For each sentence, make its syntactic Tree and dictionary and store them in lists
    syntacticTrees=[]
    dicts=[]
    for sentence in sentences:
        syntacticTree=[]
        syntacticTree, finalMessage, Do_truth_table, dict1 = MakeSyntacticTree(sentence,syntacticTree)
        if Do_truth_table==False:
            print("Sentence "+str(sentence)+" is a bad Propositional logic sentence. Process was aborted.")
            break
        syntacticTrees.append(syntacticTree)
        dicts.append(dict1)
    #Create an unified dictionary combining all dictionaries from all sentences
    new_dict = {}
    for dictionary in dicts:
        new_dict.update(dictionary)
    #Get the truth_table
    header = MakeCombinedHeader(syntacticTrees)
    Truth_table, nAtomicSentences = MakeTruthTable(new_dict, header)
    #Check if the conclusion is NOT a logical consequence from the premises (Conclusion=False while Premises=True)
    Consequence = True
    for row in Truth_table:
        values_premises = row[-num-1:-1]
        if all(value == True for value in values_premises):
            if row[-1]==False:
                Consequence = False
                break
    if Consequence == False:
        print("The Conclusion is not a logical consequence from the premises. You can find the next counter-example: ")
        for i in range(nAtomicSentences):
            print(str(header[i])+ "="+str(row[i]))
    else:
        print("The Conclusion is a logical consequence from the premises.")
    print("FINISHED")    
