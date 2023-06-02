# -*- coding: utf-8 -*-
"""
Created on Thu May 25 17:14:40 2023

@author: Evan Telford (ejt2133@columbia.edu)
"""
#%%
#load pertinent packages
import matplotlib
import sys
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
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import numpy as np
import pickle
import MP_important_functions as functions
#scikit packages
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from tqdm import tqdm
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
        self.title = 'Scikit Model Creation'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 100
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout=QGridLayout()
        self.box = QGroupBox()
        training= QLabel('Choose the training data (.pkl)') 
        training.setAlignment(Qt.AlignCenter)
        l2_button=QPushButton('Load Training Data') 
        l2_button.clicked.connect(lambda: self.load_training_data())  
        self.training = QLineEdit()
        l_button=QPushButton('Create Scikit Model') 
        l_button.clicked.connect(lambda: self.create_scikit_model()) 
        l_button.clicked.connect(lambda: self.save_training_model())  
        self.accuracy_lb= QLabel('') 
        self.accuracy_lb2=QLabel('')
        self.progress=QProgressBar()
        self.progress_p=QLabel('')
        self.layout.addWidget(training, 0,0,1,2) 
        self.layout.addWidget(self.training, 1,1,1,1)
        self.layout.addWidget(l2_button, 1,0,1,1)
        self.layout.addWidget(l_button,2,0,1,2)
        self.layout.addWidget(self.accuracy_lb,4,0,1,1)
        self.layout.addWidget(self.accuracy_lb2,4,1,1,1)
        self.layout.addWidget(self.progress, 3,0,1,1)
        self.layout.addWidget(self.progress_p, 3,1,1,1)
        self.box.setLayout(self.layout)
        self.widget=QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
    
    def load_training_data(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file')
        self.data=functions.open_dictionary(fname[0][:-4])
        self.training.setText(fname[0])
        self.fname=fname[0][0:-4].split('/')[-1]
        
    def create_training_data(self):
        data=self.data
        #create a progress bar
        progress_bar = tqdm(total=len(data), unit='Materials')
        #create new arrays for the training data
        N=500
        TD=np.zeros((len(data),N))
        Categories=np.array([])
        #loop over all materials to extract the data
        for i,crystal in enumerate(data):
            structure=data[crystal]['structure']
            analyzer=SpacegroupAnalyzer(structure)
            symmetry=analyzer.get_symmetry_dataset()
            PXRD=data[crystal]['PXRD']
            PXRD_ml_x,PXRD_ml_y=functions.generate_PXRD_data(PXRD,N)
            #populate PXRD data
            TD[i,:]=PXRD_ml_y
            Categories=np.hstack([Categories,symmetry['international']])
            progress=(i+1)/len(data) * 100
            self.progress.setValue(int(progress))
            self.progress_p.setText(str(progress)+'%')
            progress_bar.update(1)
        progress_bar.close()
            
        return TD, Categories
            
    def create_scikit_model(self): 
        #load training data
        X,Y=self.create_training_data()
        #create training and testing data sets
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        #Create and train the classifier
        classifier = RandomForestClassifier()
        classifier.fit(X_train, y_train)
        #Make predictions
        y_pred = classifier.predict(X_test)
        #Evaluate the performance
        accuracy = accuracy_score(y_test, y_pred)
        self.classifier=classifier
        self.accuracy=accuracy
        self.accuracy_lb.setText('Model Accuracy =')
        self.accuracy_lb2.setText(str(self.accuracy))

    def save_training_model(self):
        dir_name=QFileDialog.getExistingDirectory(self)
        # save model
        pickle.dump(self.classifier, open(dir_name+'/'+self.fname+'-model'+'.pkl', "wb"))
#%%
app = QApplication(sys.argv)
window = App()
window.show()
app.exec()