import xlrd
from xlwt import Workbook

def createExcel (espece, gene, meilleur):
    # choix du chemin
    #path = r"C:\chemin\vers\fichier.xls"
    
    # création 
    book = Workbook()
    
    #
     
    # création de la feuille 1
    feuil1 = book.add_sheet('feuille 1')
     
    # ajout des en-têtes
    feuil1.write(0,0,'Espèce') #ecrit dans la feuille 1 en ligne 0, col 0
    feuil1.col(0).width = 5000
    feuil1.write(0,1,'Gène') #ecrit dans la feuille 1 en ligne 0, col 1
    feuil1.col(1).width = 5000
    feuil1.write(0,2,'sgRNA') #ecrit dans la feuille 1 en ligne 0, col 2
    feuil1.col(2).width = 10000
    feuil1.write(0,3,'hit_20mer') #ecrit dans la feuille 1 en ligne 0, col 3
    feuil1.col(3).width = 5000
    feuil1.write(0,4,'hit_12mer') #ecrit dans la feuille 1 en ligne 0, col 3
    feuil1.col(4).width = 5000
    feuil1.write(0,5,'tm') #ecrit dans la feuille 1 en ligne 0, col 3
    feuil1.col(5).width = 5000

    # ajout des valeurs dans la ligne suivante
    ligne = feuil1.row(1) #ligne 1
    ligne.write(0,espece) #ligne 1 col 0
    ligne.write(1,gene) #ligne 1 col 1
    ligne.write(3,meilleur[0]['hit_20mer'])
    ligne.write(4,meilleur[0]['hit_12mer'])
    ligne.write(5,meilleur[0]['tm'])
  
    ligne = feuil1.row(4) #ligne 1
    ligne.write(3,meilleur[1]['hit_20mer'])
    ligne.write(4,meilleur[1]['hit_12mer'])
    ligne.write(5,meilleur[1]['tm'])
    
    liste = [[meilleur[0]['sequence'],[meilleur[0]["start"]]],[meilleur[1]['sequence'],[meilleur[1]["start"]]]]
    
    cpt = 0
    for i in liste: #i : liste avec 2sgRNA compl
        cpt = cpt+1
        for j in i: #j : 1sgRNA
            ligne = "ligne"+str(cpt)
            ligne = feuil1.row(cpt) 
            ligne.write(2,j) #ecriture du sgRNA
            cpt = cpt+1

    # création matérielle du fichier résultant
    #ajouter securité si possible si fichier ouvert
    try:
        book.save(espece+gene+'.xls')
    except PermissionError:
        print("permission non accordée - pensez à fermer le fichier excel")

#espece = "Vitis Vinifera"
#gene = "HT5"
#liste = [["atcg","tagc"],["ccaa","ggtt"]]



#hit_20mer,tm,hit_12mer,meilleur = 'NOPE'
#createExcel(espece, gene, liste, hit_20mer, tm, hit_12mer,test)

