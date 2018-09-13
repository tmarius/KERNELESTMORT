# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InterfaceCoutos.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import docFinal, toExcel, crisprPrototype1

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(641, 375)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(460, 230, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(460, 260, 221, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(460, 290, 151, 28))
        self.pushButton.setCheckable(False)
        self.pushButton.setChecked(False)
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(30, 30, 581, 194))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setInputMask("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_3.addWidget(self.lineEdit_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.radioButton.setChecked(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.radioButton.setText(_translate("Dialog", "sgRNA"))
        self.radioButton_2.setText(_translate("Dialog", "Séquence promotrice"))
        self.pushButton.setText(_translate("Dialog", "Valider"))
        
#       #Event permettant d'appeler la fonction on_click
        self.pushButton.clicked.connect(self.on_click)
        
        
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit.setPlaceholderText(_translate("Dialog", "Entrer la séquence partielle ..."))
        self.comboBox.setItemText(0, _translate("Dialog", "Arabidopsis thaliana"))
        self.comboBox.setItemText(1, _translate("Dialog", "Vitis vinifera"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Nom/ID NCBI du gène"))
        self.lineEdit_4.setPlaceholderText(_translate("Dialog", "5\' => 3\'"))
        self.lineEdit_3.setPlaceholderText(_translate("Dialog", "5\' => 3\' comp"))




    @pyqtSlot()
    def on_click(self):
        species = ['Arabidopsis thaliana','Vitis vinifera']
        
        
        nameID = self.lineEdit.text()
        sens = self.lineEdit_4.text()
        antisens = self.lineEdit_3.text()
        speciesIndex = self.comboBox.currentIndex()
        speciesName=species[speciesIndex]
        partialSeq = self.textEdit.toPlainText()
        choiceBox= self.radioButton.isChecked()
#        return(nameID)
        
                
        ###Initialisation de toutes les variables (, seq, id,...)
        #driver = docFinal.webdriver.Chrome()  

        driver = docFinal.webdriver.Chrome() 

        
        #Si le bouton radio est sgRNA
        if(choiceBox==True):
            if(docFinal.isTextsNotEmpty(speciesName, nameID, sens, antisens)):
                print("On fait les manip nécessaires pour la recherche sgRNA")
                CDS = docFinal.rechSgRNAGeneId(speciesName,nameID, driver)
                sgrna = crisprPrototype1.RetrouveBestSgrna(sens,antisens)
                toExcel.createExcel(speciesName, nameID, sgrna,CDS)
                
                
                
            
            elif docFinal.isTextsNotEmpty(speciesName, partialSeq, sens, antisens):
                CDS = docFinal.rechSgRNASeq(speciesName, partialSeq, driver)
                sgrna = crisprPrototype1.RetrouveBestSgrna(sens,antisens)
                toExcel.createExcel(speciesName, nameID, sgrna,CDS)
                
            else:
                print("ERREUR - Pour la recherche de sgRNA, veuillez entrer une espèce, un id, une séquence, et deux brins 5' 3'")
            
        
        #Si le bouton radio est boite de régulation
        else:    
            if(docFinal.isTextsNotEmpty(speciesName, nameID)):
                print("On fait les manip nécessaires pour la boîte de régulation")
                docFinal.rechBoitPromGeneId(speciesName, nameID, driver)
                
            elif docFinal.isTextsNotEmpty(speciesName, partialSeq):
                docFinal.rechBoitPromSeq(speciesName, partialSeq, driver)
                
            else:
                print("ERREUR - Pour la boîte de régulation, veuillez entrer une espèce, un id et une séquence")
        

        
        
        

        
        
        #radioo2= self.radioButton_2.isChecked()
        




    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    
    
    
       
# LOC100232985