# -*- coding: utf-8 -*-
"""
TASK 2
"""
def FindConnector(connector):
    found = False
    for i in range(len(string)):
        if string[i] == connector:
            found = True
            break
    if found == False:
        return False
    elif found == True:
        return True
    
def Brackets(string,p):
    sentence_1 = ""
    sentence_2 = ""
    inici = ""
    final = ""
    #Search position of closing bracket
    string_1 = string[p:]
    for z in range(len(string_1)):
        if string_1[z] == ")":
            sentence_2 = string_1[1:z]
            final = string_1[z:]
            break
    #Search position of opening bracket
    string_r = string[::-1]
    p_r = len(string)-1 - p
    string_2 = string_r[p_r:]
    for j in range(len(string_2)):
        if string_2[j] == "(":
            sentence_1 = string_2[1:j]
            inici = string_2[j:]
            sentence_1 = sentence_1[::-1]
            inici = inici[::-1]
            break
    return inici, sentence_1, sentence_2, final


def AddBrackets(string,p,connector):
    inici, sentence_1, sentence_2, final = Brackets (string,p)
    #If there are no brakets yet
    if connector != "¬":
        if sentence_1 == "" and sentence_2 == "":
            string = "("+string[:p]+")"+string[p]+"("+string[p+1:]+")"
        #If there were brackets before:
        else:
            string = inici+"("+sentence_1+")"+string[p]+"("+sentence_2+")"+final
    else: #if connector = ¬
        if sentence_2 == "":
            string = string[:p+1]+"("+string[p+1:]+")"
        else:
            string = string[:p+1]+"("+sentence_2+")"+final
    return string    


#Ask for logic sentence and connectors
program = True
print("This program will add connectors by trying to follow the user instructions.\nThe sentence must use as connectors : -|¬+& and lowercase letters as atomic sentences")
string = input("\nEnter logic sentence: ")
continuity = True
try:
    num = int(input("\nEnter number of connectors: "))
except:
    print("\nThe number is not an integer.")
    continuity=False
if continuity == True:    
    possible_connectors = ["¬","+","-","&","|"]
    connectors = []
    for i in range(num):
        connector = input("\nEnter connector "+str(i+1)+": ")
        if connector not in possible_connectors:
            print("Error: input is not valid as a connector")
            program = False
            break
        if not FindConnector(connector):
            print("Error: you gave a connector that isn't in the string.")
            program = False
            break  
        connectors.append(connector)
    
    #Start program if everything is fine
    if program == True:
        for connector in connectors:
            for i in range(len(string)):
                if string[i]==connector:
                    if string[i+1]!="(":
                        position = i
                        string = AddBrackets(string,position,connector)
                        break
        #If we have put parenthesis between atomic sentence, take them out:
        for i in range(len(string)):
            try:
                if "a"<=string[i]<="z" and string[i+1] ==")" and string[i-1] == "(":
                    string = string[:i-1] + string[i] + string[i+2:]
            except: #Out of index
                break
        #If we have put parenthesis between negation + atomic sentence, take them out:
        for i in range(len(string)):
            try:
                if "a"<=string[i]<="z" and string[i-1] == "¬" and string[i-2] == "(":
                    string = string[:i-2] + string[i-1:i+1] + string[i+2:]
            except: #Out of index
                break
        print("\n"+string+"\n")
