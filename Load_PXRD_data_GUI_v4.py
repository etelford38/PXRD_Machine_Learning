#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 09:15:06 2023

@author: Evan Telford (ejt2133@columbia.edu)
"""
#%%
#convert your files first to .xy through this: https://www.icdd.com/jade-pattern-converter/?page=www.icdd.com/JadeSAS/jade-pattern-converter/
#%%
#load pertinent packages
import pandas as pan
import numpy as np
import scipy.signal as scs
import sys
from scipy.signal import find_peaks
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib
from scipy.interpolate import UnivariateSpline
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QFileDialog,
    QWidget,
    QGroupBox,
)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import MP_important_functions as functions
#sets the default font style for matplotlib plots
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 4}
matplotlib.rc('font', **font)
matplotlib.use('Qt5Agg')
#%%
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=4, height=4, dpi=300):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        for axis in ['top','bottom','left','right']:
            self.axes.spines[axis].set_linewidth(0.5)
        self.axes.xaxis.set_tick_params(width=0.5)
        self.axes.yaxis.set_tick_params(width=0.5)
        super(MplCanvas, self).__init__(self.fig)
#%%
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__() #needed for initialization
        self.main_layout = QGridLayout() #create grid layout of entire window
        self.setWindowTitle("PXRD Plotter and Peak Finder") #creates GUI title
        self.filename=[] #sets temp variable for the file name
        self.filename_bk=[] #sets temp variable for the file name
        #create group boxes
        self.load_GUI()
        self.analysis_GUI()
        self.hyperlink_GUI()
        self.d_spacing_GUI()
        self.prediction_GUI()
        #create plot
        self.dataplot1=MplCanvas(self)
        self.toolbar1=NavigationToolbar(self.dataplot1,self)
        #Add all widgets to the overall layout
        self.main_layout.addWidget(self.hyperlinkGUI,0,0,1,1)
        self.main_layout.addWidget(self.LoadGUI,0,1,1,2)
        self.main_layout.addWidget(self.AnalysisGUI,1,0,1,3)
        self.main_layout.addWidget(self.dspaceGUI,0,3,1,1)
        self.main_layout.addWidget(self.PredictionGUI,1,3,1,1)
        self.main_layout.addWidget(self.dataplot1,2,0,1,4)
        self.main_layout.addWidget(self.toolbar1,3,0,1,4)
        #create the main layout
        self.widget=QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        
    def getfile(self): #opens window to find and select files
        fname=QFileDialog.getOpenFileName(self, 'Open file')
        self.filename.setText(fname[0])
        
    def getfile_bk(self): #opens window to find and select files
        fname=QFileDialog.getOpenFileName(self, 'Open file')
        self.filename_bk.setText(fname[0])
    
    def getmodel(self): 
        fname=QFileDialog.getOpenFileName(self, 'Open file')
        self.modelname.setText(fname[0])
        
    def load_data(self,name):
        file=pan.read_csv(name, header=None, delimiter='\t',skiprows=2)
        self.PXRD={'2Theta':file[0],'Intensity':file[1]}
        #scale the intensity
        self.PXRD['Intensity']=self.PXRD['Intensity']/np.max(self.PXRD['Intensity'])
        
    def load_background(self,name): #loads any quantum design data file
        file=pan.read_csv(name, header=None, delimiter='\t',skiprows=2)
        self.PXRD_bk={'2Theta':file[0],'Intensity':file[1]}
        #scale the intensity
        self.PXRD_bk['Intensity']=self.PXRD_bk['Intensity']/np.max(self.PXRD_bk['Intensity'])
    
    def load_model(self,name): #loads any quantum design data file
        self.model=functions.open_dictionary(name[0:-4])
        
    def plot_data(self,x,y,lb):
        self.dataplot1.axes.cla()
        self.dataplot1.axes.plot(x,y,linewidth=0.5,label=lb)
        self.dataplot1.axes.set_xlim(0,90)
        self.dataplot1.axes.set_ylim(-0.1,1.1)
        self.dataplot1.axes.tick_params(direction="in")
        self.dataplot1.axes.yaxis.set_ticks_position('both')
        self.dataplot1.axes.xaxis.set_ticks_position('both')
        self.dataplot1.axes.grid(linewidth=0.25,color='k',linestyle='--')
        self.dataplot1.axes.set_xlabel(r'$2\theta\ (^\circ)$',labelpad=0.1)
        self.dataplot1.axes.set_ylabel(r'$Intensity\ (a.u.)$',labelpad=0.1)
        self.dataplot1.fig.tight_layout()
        self.dataplot1.axes.legend(fontsize=3)
        self.dataplot1.draw()
        
    def update_plot(self,x,y,lb):
        self.dataplot1.axes.plot(x,y,linewidth=0.5,label=lb)
        self.dataplot1.axes.set_xlim(0,90)
        self.dataplot1.axes.set_ylim(-0.1,1.1)
        self.dataplot1.axes.legend(fontsize=3)
        self.dataplot1.draw()
        
    def update_plot_peaks(self,x,y,lb):
        self.dataplot1.axes.plot(x,y,'+',markersize=5,label=lb)
        self.dataplot1.axes.legend(fontsize=3)
        self.dataplot1.draw()
        
    def create_testing_data(self):
        #extract scaling and binning windows
        self.scaling=float(self.scale_value.text()) if len(self.scale_value.text())>0 else 1
        self.binning=int(self.bin_text.text()) if len(self.scale_value.text())>0 else int(3)
        #set the box values to the scaling and binning window sizes
        self.scale_value.setText(str(self.scaling))
        self.bin_text.setText(str(self.binning))
        #determine data
        xt=self.PXRD['2Theta']
        if self.check.isChecked():
            yt=self.PXRD['Intensity']-scs.savgol_filter(self.PXRD_bk['Intensity']*self.scaling,self.binning,1)
        else:
            yt=self.PXRD['Intensity']
        fit=UnivariateSpline(x=xt, y=yt,k=1)
        fit.set_smoothing_factor(0.0)
        TT=np.linspace(5,90,500)
        IT=fit(TT)
        self.PXRD_ML={'2Theta':TT,'Intensity':IT}
        
    def find_peaks(self,x,y):
        #extract peak fitting parameters
        width=float(self.width.text()) if len(self.width.text())>0 else float(0.1)
        prominence=float(self.prominence.text()) if len(self.prominence.text())>0 else float(0.1)
        distance=float(self.distance.text()) if len(self.distance.text())>0 else float(0.5)
        threshold=float(self.threshold.text()) if len(self.threshold.text())>0 else float(0.0)
        #set the box values to extracted peak fitting parameters
        self.width.setText(str(width))
        self.prominence.setText(str(prominence))
        self.distance.setText(str(distance))
        self.threshold.setText(str(threshold))
        theta_scale=len(x)/(np.max(x)-np.min(x))
        peaks, _ = find_peaks(y, prominence=prominence,width=width*theta_scale,distance=distance*theta_scale,threshold=threshold)
        self.peaks={'2Theta':x[peaks],'Intensity':y[peaks]}
        
    def load_GUI(self): #creates the load data GUI
        layout = QGridLayout()
        self.LoadGUI = QGroupBox('Load PXRD Data (xy format)') 
        #Create new widget to load data
        self.filename = QLineEdit()
        l2_button=QPushButton('Load Data')
        l2_button.clicked.connect(self.getfile)
        #Create new widget to load data
        self.filename_bk = QLineEdit()
        l3_button=QPushButton('Load Background Data')
        l3_button.clicked.connect(self.getfile_bk)
        l4_button=QPushButton('Import Data')
        l4_button.clicked.connect(lambda: self.load_data(self.filename.text()))
        l4_button.clicked.connect(lambda: self.load_background(self.filename_bk.text()) if self.check.isChecked() else print('no background file used'))
        self.check=QCheckBox('Load Background Data?')
        #adds widgets
        layout.addWidget(self.filename, 0,1) 
        layout.addWidget(l2_button, 0,0)
        layout.addWidget(self.filename_bk, 1,1) 
        layout.addWidget(l3_button, 1,0)
        layout.addWidget(self.check,2,0)
        layout.addWidget(l4_button, 3,0,1,2)
        self.LoadGUI.setLayout(layout)
        
    def analysis_GUI(self):
        layout = QGridLayout()
        self.AnalysisGUI = QGroupBox('PXRD Analysis Settings') 
        #Create parameters for scaling and smoothing the data
        self.scaling=[]
        self.binning=[]
        #default scaling and binning values
        self.scaling=1
        self.binning=3
        #create GUI windows
        scale_text=QLabel('Background Scaling Value (default: 1)')
        scale_text.setAlignment(Qt.AlignCenter)
        self.scale_value=QLineEdit()    
        bin_text=QLabel('Binning Window for Smoothing Background (default: 3)')
        bin_text.setAlignment(Qt.AlignCenter)
        self.bin_text=QLineEdit()
        #peak finding GUI entries
        width_text=QLabel('Peak Width (2 Theta)')
        width_text.setAlignment(Qt.AlignCenter)
        prominence_text=QLabel('Peak Prominence')
        prominence_text.setAlignment(Qt.AlignCenter)
        peak_text=QLabel('Peak Distance (2 Theta)')
        peak_text.setAlignment(Qt.AlignCenter)
        threshold_text=QLabel('Threshold Distance')
        threshold_text.setAlignment(Qt.AlignCenter)
        self.width=QLineEdit()    
        self.prominence=QLineEdit()    
        self.distance=QLineEdit()     
        self.threshold=QLineEdit()    
        #create the buttons
        l4_button=QPushButton('Generate Data')
        l4_button.clicked.connect(lambda: self.create_testing_data())
        l4_button.clicked.connect(lambda: self.plot_data(self.PXRD['2Theta'],self.PXRD['Intensity'],'Raw data'))        
        l4_button.clicked.connect(lambda: self.update_plot(self.PXRD_bk['2Theta'],self.PXRD_bk['Intensity'],'Background') if self.check.isChecked() else print('no background file used'))
        l4_button.clicked.connect(lambda: self.update_plot(self.PXRD['2Theta'],self.PXRD['Intensity']-self.PXRD_bk['Intensity'],'Raw data minus background') if self.check.isChecked() else print('no background file used'))
        l4_button.clicked.connect(lambda: self.update_plot(self.PXRD_ML['2Theta'],self.PXRD_ML['Intensity'],'Testing data'))
        l5_button=QPushButton('Fit Peaks')
        l5_button.clicked.connect(lambda: self.find_peaks(self.PXRD_ML['2Theta'],self.PXRD_ML['Intensity']))
        l5_button.clicked.connect(lambda: self.update_plot_peaks(self.peaks['2Theta'],self.peaks['Intensity'],'Extracted peaks'))
        #adds widgets
        layout.addWidget(scale_text, 0,0,1,2) 
        layout.addWidget(self.scale_value, 1,0,1,2)
        layout.addWidget(bin_text, 0,2,1,2) 
        layout.addWidget(self.bin_text, 1,2,1,2)
        layout.addWidget(width_text,3,0,1,1)
        layout.addWidget(prominence_text,3,1,1,1)
        layout.addWidget(peak_text,3,2,1,1)
        layout.addWidget(threshold_text,3,3,1,1)
        layout.addWidget(self.width,4,0,1,1)
        layout.addWidget(self.prominence,4,1,1,1)
        layout.addWidget(self.distance,4,2,1,1)
        layout.addWidget(self.threshold,4,3,1,1)
        layout.addWidget(l4_button, 2,0,1,4)
        layout.addWidget(l5_button, 5,0,1,4)
        self.AnalysisGUI.setLayout(layout)
        
    def d_spacing_GUI(self):
        layout= QGridLayout()
        self.dspaceGUI = QGroupBox('D Spacings')
        #create boxes
        l_button=QPushButton('Calculate D Spacings')
        l_button.clicked.connect(lambda: self.update_dspacings())
        thetas=QLabel('2 Theta Values')
        self.thetas=QComboBox()
        dspacings=QLabel('D/n Values')
        self.dspacings=QComboBox()
        #set layout
        layout.addWidget(l_button,0,0,2,2)
        layout.addWidget(thetas,2,0,1,1)
        layout.addWidget(self.thetas,2,1,1,1)
        layout.addWidget(dspacings,3,0,1,1)
        layout.addWidget(self.dspacings,3,1,1,1)
        self.dspaceGUI.setLayout(layout)
        
    def update_dspacings(self):
        theta=(self.peaks['2Theta']/2) * (np.pi/180) #convert degrees to radians
        wavelength=1.315 #copper K-alpha radiation wavelentgh
        ds=wavelength/(2*np.sin(theta))
        x_items=[str(x) for x in self.peaks['2Theta']]
        ds=[str(x) for x in ds]
        self.thetas.clear()
        self.dspacings.clear()
        self.thetas.addItems(x_items)
        self.dspacings.addItems(ds)
        
    def hyperlink_GUI(self):
        layout= QGridLayout()
        self.hyperlinkGUI = QGroupBox('Online Data Converter')
        #create hypderlink GUI
        label=QLabel()
        label.setText('<a href="https://www.icdd.com/jade-pattern-converter/?page=www.icdd.com/JadeSAS/jade-pattern-converter/">Online Converter</a>')
        label.setAlignment(Qt.AlignCenter)
        label.setOpenExternalLinks(True)
        label.linkActivated.connect(self.open_link)
        #set layout
        layout.addWidget(label,0,0)
        self.hyperlinkGUI.setLayout(layout)
        
    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))
        
    def prediction_GUI(self):
        layout = QGridLayout()
        self.PredictionGUI = QGroupBox('Predict Crystal Structure') 
        #Create new widget to load data
        self.modelname= QLineEdit()
        l1_button=QPushButton('Load Model')
        l1_button.clicked.connect(lambda: self.getmodel())
        l1_button.clicked.connect(lambda: self.load_model(self.modelname.text()))
        # L1=QLabel('Structure Prediction')
        self.prediction_widget=QLabel('')
        l2_button=QPushButton('Predict Structure')
        l2_button.clicked.connect(lambda: self.predict_structure())
        l2_button.clicked.connect(lambda: self.update_plot(self.predict_x,self.predict_y,'Prediction data'))
        #adds widgets 
        layout.addWidget(self.modelname, 0,1) 
        layout.addWidget(l1_button, 0,0)
        layout.addWidget(l2_button, 1,0,1,1)
        # layout.addWidget(L1,2,0,1,1)
        layout.addWidget(self.prediction_widget,1,1,1,1)
        self.PredictionGUI.setLayout(layout)
        
    def predict_structure(self):   
        sigma=0.2
        gamma=0.1
        N=500
        x,y = np.array(self.peaks['2Theta']), np.array(self.peaks['Intensity'])
        self.predict_x,self.predict_y=functions.generate_PXRD_voigt(x,y,sigma,gamma,N)
        # Make predictions on the test set
        y_pred_prob = self.model.predict_proba(self.predict_y.reshape(1, -1))
        # Get the top three most likely classes for each sample
        top_three_classes = np.argsort(-y_pred_prob, axis=1)[:, :3]
        # Map the indices to the actual class labels
        class_labels = self.model.classes_
        top_three_labels = class_labels[top_three_classes]
        self.prediction_widget.setText('The most likely structures are ' + str(top_three_labels[0]))
#%%
#This is the actual code to run the gui       
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()