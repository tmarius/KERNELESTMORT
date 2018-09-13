# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 14:01:45 2018

@author: ivan
"""

import time
import json
from os import chdir,getcwd,remove 
import toExcel

def reverse(chaineantisens):
    chainesens = ""#chaine inversée
     
    for lettre in reversed(chaineantisens):
        chainesens += lettre
         
    return(chainesens)

    
def deuxMaxTm(objectswithtmlist):
    list2max=[]    
    tmp = float('0')
    for objectwithtmlist in objectswithtmlist:
        tmp = float(objectwithtmlist['tm'])
        print(tmp)
        
        if (len(list2max) == 0):
            list2max.append(objectwithtmlist)    
           
        elif (len(list2max) == 1):
            if tmp >= float(list2max[0]['tm']):
                list2max.append(list2max[0]) 
                list2max[0] = objectwithtmlist
            else:
                list2max.append(objectwithtmlist)
        else:
            if tmp >= float(list2max[0]['tm']):
                list2max[1] = list2max[0]
                list2max[0] = objectwithtmlist
            elif tmp >= float(list2max[1]['tm']):
                list2max[1] = objectwithtmlist
    return(list2max)


def complementaire(seq):
    compl = ''
    for i in seq:
        if i == 'A':
            compl += 'T'
        elif i == 'T':
            compl += 'A'
        elif i == 'C':
            compl += 'G'
        elif i == 'G':
            compl += 'C'
        else:
            print ('sequence corompue')
    return (compl)


def loadFile():
    path = getcwd(); 
    path = path + '\\tmp' ;
    config = json.loads(open(path+'\CRISPRdirect.json').read())
    results=config['results']
    return (results)


def InitSelectionSgrna(results):
    liste = [{'end': '38', 'gc': '85.00', 'hit_12mer': '999', 'hit_20mer': '999', 'hit_8mer': '81', 'resite': ['BsiEI', 'EaeI', 'EagI'], 'sequence': 'TTCGCGGCCCCGTCGGCCGGTGG', 'start': '16', 'strand': '+', 'tm': '89.75', 'tttt': '0'}, {'end': '26', 'gc': '75.00', 'hit_12mer': '999', 'hit_20mer': '999', 'hit_8mer': '326', 'resite': [], 'sequence': 'CCTGCTGGAGGATTCGCGGCCCC', 'start': '4', 'strand': '-', 'tm': '84.61', 'tttt': '0'}]
    return (liste)
    
#    Compare le 1er et le 2eme grace a la fonction lemeilleur
#    les mets dans l ordre
#    compare le deuxieme avec la liste, si le deuxieme est battue compare avec le 1er
#    si c est bon remplace dans la liste des meilleur
#    retourne la liste de deux

#Compare 2 sgnrra en fonction de critere => critere en string, nom de la colonne
    #RESULTAT 1 => la premiere sequence est mieux
#    2 => La deuxieme sequence est mieux
#    3 => IDEM
def comparaison(sgnra1,sgnra2,critere):    
    if float(sgnra1[critere]) < float(sgnra2[critere]):
        return 1
    elif float(sgnra1[critere]) > float(sgnra2[critere]):
        return 2
    else:
        return 3

 #Compare 2 sgnra 
    #RESULTAT 1 => la premiere sequence est mieux
#    2 => La deuxieme sequence est mieux
   
def leMeilleur(sgnra1,sgnra2):
    if (comparaison(sgnra1,sgnra2,'hit_20mer')==1):
        return 1
    elif (comparaison(sgnra1,sgnra2,'hit_20mer')==2):
        return 2
    elif (comparaison(sgnra1,sgnra2,'hit_20mer')==3):
        if (comparaison(sgnra1,sgnra2,'hit_12mer')==1):
            return 1
        if (comparaison(sgnra1,sgnra2,'hit_12mer')==2):
            return 2
        elif (comparaison(sgnra1,sgnra2,'hit_12mer')==3):
            if (comparaison(sgnra1,sgnra2,'tm')==1):
                return 2
            elif (comparaison(sgnra1,sgnra2,'tm')==2):
                return 1

def RetrouveBestSgrna(sens,antisens):
    results = loadFile()
    meilleur = InitSelectionSgrna(results)
    for sgrna in results: 
        if not (sgrna['hit_12mer'] == '0' or sgrna['hit_20mer'] == '0' or sgrna['tm'] < '65.00'):
            if (leMeilleur(meilleur[1],sgrna)==2):
                if (leMeilleur(meilleur[0],sgrna)==2):
                    meilleur[0]=sgrna
                else :
                    meilleur[1]=sgrna
    traitement(meilleur,sens,antisens)                
    return (meilleur)            




#Best = leMeilleur(results[0],results[2])
#print (Best) 


#for result in results:
#    #specificité
#    if((int(result['hit_20mer']) <= 1) and (int(result['hit_12mer']) <=1)):
#        specificresults.append(result)
#        
#    
#        
#        
#sgrnalist=deuxMaxTm(specificresults)
#
    
# Retroune la sequence si en stand -. cree le complementaire dans hit-8mer
def traitement(meilleur, sens, antisens):    
    for sgrna in meilleur:  
#        stringlistsgrnacomps=[]
        if(sgrna['strand'] == '-'):
            
            seq = (reverse(sgrna['sequence']))
            sgrna['sequence']=seq
        else :  
            seq = sgrna['sequence'] 
            
        seq_comp =  complementaire(sgrna['sequence'])
        
        seq = "5'-"+sens+ seq +"-3'"
        sgrna['sequence'] = seq
        seq_comp =  reverse(seq_comp)   
        seq_comp = "5'-"+antisens+ seq_comp +"-3'"
        sgrna['start'] = seq_comp
        
        
    path = getcwd(); 
    path = path + '\\tmp' ;
    remove(path+'\CRISPRdirect.json')    

    
        
#        else:
#            stringlistsgrnacomps.append(sgrna['sequence'])
#        stringlistsgrnacomps.append(complementaire(sgrna['sequence']))
#        allstringlistsgrna.append(stringlistsgrnacomps)
#    print(allstringlistsgrna)     

#SEQ => 6 => RETOURNE => COMPLEMENTAIRE => ETIQUETTE => TABLEAU

#test = RetrouveBestSgrna()
#traitement (test)
#print (test)
#espece = "Vitis Vinifera"
#gene = "HT5"
#tm,hit_12mer,meilleur = 'NOP'
#liste = []
#hit_20mer = []
#print (test[0]["hit-8mer"])
#toExcel.createExcel(espece, gene, test)