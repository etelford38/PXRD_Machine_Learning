# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:42:12 2023

@author: Evan Telford (ejt2133@columbia.edu)
"""
#%%
#load pertinent packages
import MP_important_functions as FUNC
import sys
import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QGridLayout,
    QWidget,
    QGroupBox,
    QFileDialog
)
#sets the default font style for matplotlib plots
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 4}
matplotlib.rc('font', **font)
matplotlib.use('Qt5Agg')
#%%
class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'Materials Project Downloader'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 100
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout=QGridLayout()
        self.box = QGroupBox()
        elements= QLabel('Enter the Desired Elements (X,Y,Z,...)') 
        elements.setAlignment(Qt.AlignCenter)
        self.elements = QLineEdit()
        self.progress=QProgressBar()
        self.progress_p=QLabel('')
        l_button=QPushButton('Download Database') 
        l_button.clicked.connect(lambda: self.download_database())  
        self.layout.addWidget(elements, 0,0,1,2) 
        self.layout.addWidget(self.elements, 1,0,1,2)
        self.layout.addWidget(l_button, 2,0,1,2)
        self.layout.addWidget(self.progress, 3,0,1,1)
        self.layout.addWidget(self.progress_p, 3,1,1,1)
        self.box.setLayout(self.layout)
        self.widget=QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
    def download_database(self):
        text=self.elements.text()
        name=text.replace(',','-')
        text=text.split(',')
        dir_name=QFileDialog.getExistingDirectory(self)
        #access the database to generate information
        data=FUNC.return_MD(text)
        #create the final dictionary
        data_dic={}
        #loop through all compiled materials and add the information to the dictionary
        for i,crystals in enumerate(data):
            #find the material id
            iden=crystals.material_id
            structure=crystals.structure
            symm=crystals.symmetry
            elements=crystals.elements
            #determine the diffraction pattner
            pattern=FUNC.generate_PXRD(iden)
            data_dic[iden]={'structure':structure,'symmetry':symm,'elements':elements,'PXRD':pattern}
            progress=(i+1)/len(data) * 100
            self.progress.setValue(int(progress))
            self.progress_p.setText(str(progress)+'%')
        save_data=data_dic 
        FUNC.save_dictionary(save_data,dir_name+'/'+name+'-materials')
#%%       
app = QApplication(sys.argv)
window = App()
window.show()
app.exec()