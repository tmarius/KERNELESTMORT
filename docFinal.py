# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 14:29:26 2018
@author: clarisse
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from os import chdir,getcwd 
import time
import re
import json


#####################################################FIND GENE ID#########################"

def searchByNameId(espece, nameId,driver):
    driver.get("https://www.ncbi.nlm.nih.gov/gene/")
    elem = driver.find_element_by_id("term")
    elem.send_keys(espece + ' ' + nameId)
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    
    #attendre que l'utilisateur sélectionne un gène
    i=0
    while i<50:
        try:
            time.sleep(5)
            chaine_id = driver.find_element_by_xpath("//span[contains(@class,'geneid')]").text
            break
        except NoSuchElementException:
            i=i+1
            
    motif = re.compile(r'(?<=Gene ID: )[0-9]+')
    gene_id = motif.search(chaine_id)
    gene_id = gene_id.group(0)
    return (gene_id)

def searchBySeq(espece, seq, driver):
    
    if espece == "Vitis vinifera":
        espece = "Vitis vinifera (taxid:29760)"
    
    if espece == "Arabidopsis thaliana":
        espece = "Arabidopsis thaliana (taxid:3702)"
    
    driver.get("https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome")
    elem = driver.find_element_by_id("seq")
    elem.send_keys(seq)
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    elem = driver.find_element_by_id("qorganism")
    elem.send_keys(espece)
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    try:
        driver.find_element_by_id("b1").click()
    except NoSuchElementException:
        pass
    
    #attendre que l'utilisateur sélectionne un gène
    i=0
    while i<50:
        try:
            time.sleep(60)
            driver.switch_to_window(driver.window_handles[1])
            chaine_id = driver.find_element_by_xpath("//p[contains(@class,'itemid')]").text
            break
        except IndexError:
            i=i+1
            print(i)

    motif = re.compile(r'(?<=GenBank: )([A-Za-z]|[0-9])+')
    gene_id = motif.search(chaine_id)
    gene_id = gene_id.group(0)
    return (gene_id)


#########################################################FIND CDS##########################################
    

def findCDS(gene_id, driver):
    driver.get("https://www.ncbi.nlm.nih.gov/gene/")
    query = driver.find_element_by_id("term")
    query.send_keys(gene_id)
    query.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='proteinTblId']/tbody//td[contains(text(), 'mRNA')]/following-sibling::td"))
    )
    #Recupere le premier mRNA car souvent le bon, a verifié => Sinon faire comme au dessus et demander selection
    mrna = driver.find_element_by_xpath("//*[@id='proteinTblId']/tbody//td[contains(text(), 'mRNA')]/following-sibling::td").text
    mrna = driver.find_element_by_xpath("//*[@id='proteinTblId']/tbody//td[contains(text(), 'mRNA')]/following-sibling::td/a").click()
    #PARTIE 1
    #Permet de récupérer les positions de début et fin du CDS
    #On a par exemple CDS 55..1870 , on veut que begin=55 et end=1870
    driver.get("https://www.ncbi.nlm.nih.gov/nuccore/66016960")
    genbankID=driver.find_element_by_xpath("//p[contains(@class,'itemid')]").text
    #print(genbankID)
    
    motif = re.compile(r'(?<=GenBank: )([A-Za-z]|[0-9]|.)+')
    geneID = motif.search(genbankID)
    geneID = geneID.group(0)
    #print (geneID)
    cdsID="feature_"+geneID+"_CDS_0"
    #print(cdsID)
    
    

    time.sleep(5)
    positions=driver.find_element_by_xpath("//span[@id='%s']" %cdsID).text
    
    #print(positions)
    motif = re.compile(r'((\d+)\.\.(\d+))', re.IGNORECASE)
    res = motif.search(positions)
    res = res.group(0)
    #print("res : "+res)
    debutmotif = re.compile(r'(([0-9]+)(?=.))')
    finmotif = re.compile(r'((?<=..)[0-9]+)')
    debut= debutmotif.search(res)
    fin= finmotif.search(res)
    debut= debut.group(0)
    fin= fin.group(0)
    #print(debut)
    #print(fin)  
    dropdown = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "EntrezSystem2.PEntrez.Nuccore.Sequence_ResultsPanel.Sequence_SingleItemSupl.Sequence_ViewerGenbankSidePanel.Sequence_ViewerChangeRegion.Shutter"))
    )
    dropdown.click()
    selected = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "crselregion"))
    )
    selected.click()
    debinput = driver.find_element_by_id("crfrom")
    debinput.send_keys(debut)
    fininput = driver.find_element_by_id("crto")
    fininput.send_keys(fin)
    upd = driver.find_element_by_id("updateselregion").click()
    tofasta = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "ReportShortCut6"))
    )
    tofasta.click()
    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//pre"))
    )
    #sequence = driver.find_element_by_xpath("//*[@id='viewercontent1']")
    #PARTIE 2
    #Permet de récuperer le CDS en fasta
#    driver.get("https://www.ncbi.nlm.nih.gov/nuccore/AY538261.1?report=fasta&from=55&to=1665")
    seq=driver.find_element_by_xpath("//pre").text
    return (seq)

#######################################################MOITIER SUP#########################################
def moitieCDS(seq, driver):
    long = len(seq)
    longmoitie = int(long/2)
    moitie = seq[0:longmoitie]
    return (moitie)


#######################################################CRISPR SGRNA###########################################
#def findSGRNA(seq, driver):
#    
#    #Change le path de download
#    path = getcwd(); 
#    path = path + '\\tmp' ;
#    #print (path);
#    
#    chrome_options = webdriver.ChromeOptions()
#    prefs = {'download.default_directory' : path }
#    chrome_options.add_experimental_option('prefs', prefs)
#    driver = webdriver.Chrome(chrome_options=chrome_options)
#
#    driver.get("https://crispr.dbcls.jp/")
#    
##    seq="ATGATTCATTCAATTGTTGGTGCCATTACTGGCGAAAATGATAAGAAGAAGATCAAGGGAACTGTTGTGTTGATGAAGAAGAATGTGTTGGATTTTAATGACTTCAATGCATCGGTTCTGGACCGGGTTCATGAGCTGTTGGGACAGGGAGTCTCTCTGCAGCTCGTCAGTGCTGTTCATGGTGATCCTGCAAATGGGTTACAGGGGAAACTTGGGAAACCAGCATACTTGGAAGACTGGATTACCACAATTACTTCTTTAACCGCTGGCGAGTCTGCATTCAAGGTCACGTTCGACTGGGATGAGGAGATTGGAGAGCCAGGGGCTTTCATAATTAGAAACAATCACCACAGTGAGTTTTACCTCAGGACTCTCACTCTTGAAGATGTTCCTGGGTGTGGCAGAATTCA CTTTGTTTGTAATTCCTGGGTCTACCCTGCTAAGCACTACAAAACTGACCGTGTTTTCTTCACTAATCAGACATATCTTCCAAGTGAAACACCAGGGCCACTGCGCAAGTACAGAAAAGGGGAACTGGTGAATCTGAGGGGAGATGGAACCGGAGAGCTTAAGGAATGGGATCGAGTGTATGACTATGCTTACTATAATGATTTGGGGAATCCAGACAGGGATCTCAAATACGCCCGCCCTGTGCTGGGAGGATCTGCAGAGTATCCTTATCCCAGGAGGGGAAGAACTGGTAGACCACCATCTGAAAAAGATCCCAACACCGAGAGCAGATTGCCACTTGTGATGAGCTTAAACATATATGTTCCAAGAGATGAACGATTTGGTCACCTCAAGATGTCAGACTTCCTGGCTTATGCCCTGAAATCCATAGTTCAATTCCTTCTCCCTGAGTTTGAGGCTCTATGTGACATCACCCCCAATGAGTTTGACAGCTTCCAAGATGTATTAGACCTCTACGAAGGAGGAATCAAGGTCCCAGAGGGCCCTTTACTTGACAAAATTAAGGACAACATCCCTCTTGAGATGCTCAAGGAACTTGTTCGTACTGATGGGGAACATCTCTTCAAGTTCCCAATGCCCCAAGTCATCAAAGAGGATAAGTCTGCATGGAGGACTGACGAAGAATTTGCTAGAGAAATGCTGGCTGGACTCAACCCAGTTGTCATCCGACTACTCCAAGAGTTTCCTCCAAAAAGCAAGCTGGATCCTGA"
##    
#    elemchampseq = driver.find_element_by_id("useq")
#    elemchampseq.clear()
#    elemchampseq.send_keys(seq)
#    elemspecificitycheck = driver.find_element_by_id("crisprdirect-combobox-dblist-inputEl")
#    elemspecificitycheck.clear()
#    elemspecificitycheck.send_keys("Grape (Vitis vinifera) genome, IGGP_12x (Jun, 2011)")
#    elemspecificitycheck.send_keys(Keys.RETURN)
#    
#    #driver.find_element_by_xpath("//div[contains(@id,'boundlist-1010-listEl')]/ul/li").click()
#    
#    driver.find_element_by_xpath("//*[@id='ext-gen1018']/form/div[1]/p[5]/input").click()
#    #driver.find_element_by_xpath("//input[contains(@type,'submit')]")
#    element = WebDriverWait(driver, 5).until(
#            EC.presence_of_element_located((By.XPATH, "//*[@id='ext-gen1018']/form/div[4]/ul/li[2]/a[2]"))
#    )
#    element.click()
#    #driver.find_element_by_xpath("//*[@id='ext-gen1018']/form/div[4]/ul/li[2]/a[2]").click()
#    time.sleep(5)
#    config = json.loads(open(path+'\CRISPRdirect.json').read())
#    results=config['results']


#######################################################SEQUENCES PROMOTRICES##############################################


def sequencePromotrice(gene_id, CDS, driver):
    driver.get("https://www.ncbi.nlm.nih.gov/gene/")
    query = driver.find_element_by_id("term")
    query.send_keys(gene_id)
    query.send_keys(Keys.RETURN)

    element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "button-1082"))
    )
    element.click()
    driver.find_element_by_id("menuitem-1038-itemEl").click()
    element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='seq-panel_0-body']/table/tbody/tr/td[2]/div"))
    )
    #seq : enlever les retour à la ligne
    seq = driver.find_element_by_xpath("//*[@id='seq-panel_0-body']/table/tbody/tr/td[2]/div").text 
    regle = re.compile(r'[\n]')
    fasta = regle.sub("",seq)
    #CDS : enlever le début representant les info FASTA et les retour a la ligne
    regle = re.compile(r'[\n]')
    CDS = regle.sub("",CDS)
    motifCDS = re.compile(r'(ATG[ACTG]+)')
    CDS = motifCDS.search(CDS)
    CDS = CDS.group(0)
    CDS = CDS[0:10]
    #recupérer les séquences promotrices
    motifPromot = re.compile(r'(([ATGC]+)(?='+CDS+'))')
    res = motifPromot.search(fasta)
    res = res.group(0)
    if len(res) > 2000:
        coup = len(res) - 2000
        res =  res[coup:len(res)]
    return(res)
    
def boiteProm(seqProm, driver):
    driver.get("https://sogo.dna.affrc.go.jp/cgi-bin/sogo.cgi?lang=en&pj=640&action=page&page=newplace")
    query = driver.find_element_by_xpath("//*[@id='content']/form/textarea")
    query.send_keys(seqProm)
    driver.find_element_by_xpath("//*[@id='content']/form/input[5]").click()
    

    
#######################################################DEBUT PROGRAMME##############################################

def rechSgRNASeq(espece,seq, driver):
     
    gene_id = searchBySeq(espece,seq, driver)
    CDS = findCDS(gene_id, driver)
    CDSmoit = moitieCDS(CDS, driver)
    findSGRNA(CDSmoit, driver)

def rechSgRNAGeneId(espece,gene, driver):
    gene_id = searchByNameId(espece,gene, driver)
    CDS = findCDS(gene_id, driver)
    CDSmoit = moitieCDS(CDS, driver)
    findSGRNA(CDSmoit, driver)
    return(CDS)
    
def rechBoitPromSeq(espece,seq, driver):
    gene_id = searchByNameId(espece,seq, driver)
    CDS = findCDS(gene_id, driver)
    CDSmoit = moitieCDS(CDS, driver)
    seqProm = sequencePromotrice(gene_id,CDSmoit, driver)
    boiteProm(seqProm, driver)
    
def rechBoitPromGeneId(espece,gene, driver):
    gene_id = searchByNameId(espece,gene, driver)
    CDS = findCDS(gene_id, driver)
    CDSmoit = moitieCDS(CDS, driver)
    seqProm = sequencePromotrice(gene_id,CDSmoit, driver)
    boiteProm(seqProm, driver)
    
#######################################################CRISPR SGRNA###########################################
def findSGRNA(seq, driver):
    
    #Change le path de download
    path = getcwd(); 
    path = path + '\\tmp' ;
    print (path);
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : path }
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    driver.get("https://crispr.dbcls.jp/") 
  
    elemchampseq = driver.find_element_by_id("useq")
    elemchampseq.clear()
    elemchampseq.send_keys(seq)
    elemspecificitycheck = driver.find_element_by_id("crisprdirect-combobox-dblist-inputEl")
    elemspecificitycheck.clear()
    elemspecificitycheck.send_keys("Grape (Vitis vinifera) genome, IGGP_12x (Jun, 2011)")
    elemspecificitycheck.send_keys(Keys.RETURN)
     
#    driver.find_element_by_xpath("//*[@id='ext-gen1018']/form/div[1]/p[5]/input").click()
#    time.sleep(1)
    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='ext-gen1018']/form/div[1]/p[5]/input"))
    )
    driver.find_element_by_xpath("//*[@id='ext-gen1018']/form/div[1]/p[5]/input").click()
    
    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='ext-gen1018']/form/div[4]/ul/li[2]/a[2]"))
    )
    driver.find_element_by_xpath("//*[@id='ext-gen1018']/form/div[4]/ul/li[2]/a[2]").click()
    time.sleep(20)
    config = json.loads(open(path+'\CRISPRdirect.json').read())
    results=config['results']
    

#################################################
#driver = webdriver.Chrome() 
#espece = "Vitis vinifera"
#seq = "atgcct gctggaggat tcgcggcccc gtcggccggt ggcgactttg aagccaagat cactcctatc gttatcattt cttgcatcat ggccgccacc ggcggcctca tgttcggcta cgacgtt"
#gene = "Vvht5"

##rechSgRNASeq(espece,seq)
#rechSgRNAGeneId(espece,gene)
##rechBoitPromSeq(espece,seq)
##rechBoitPromGeneId(espece,gene)
#sgrna = crisprPrototype1.RetrouveBestSgrna()
#print (sgrna)
#toExcel.createExcel(espece, gene, sgrna)

#espece = ""
#seq = "atgcct gctggaggat tcgcggcccc gtcggccggt ggcgactttg aagccaagat cactcctatc gttatcattt cttgcatcat ggccgccacc ggcggcctca tgttcggcta cgacgtt"
#gene = "Vvht5"

#rechSgRNASeq(espece,seq)
#rechSgRNAGeneId(espece,gene)
#rechBoitPromSeq(espece,seq)
#rechBoitPromGeneId(espece,gene)
##########################################















#Si au moins une chaine de caractère passée est vide, retourne false. Sinon, retourne true
def isTextsNotEmpty(*args):
    result=True
    for arg in args:
        if not arg:
            result=False
    return result
