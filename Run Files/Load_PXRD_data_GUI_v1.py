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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib
from scipy.interpolate import UnivariateSpline
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QFileDialog,
    QWidget,
    QGroupBox,
    QMainWindow
)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
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
        #create plot
        self.dataplot1=MplCanvas(self)
        self.toolbar1=NavigationToolbar(self.dataplot1,self)
        #Add all widgets to the overall layout
        self.main_layout.addWidget(self.hyperlinkGUI,0,0,1,1)
        self.main_layout.addWidget(self.LoadGUI,0,1,1,3)
        self.main_layout.addWidget(self.AnalysisGUI,1,0,1,4)
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
        
    def load_data(self,name): 
        file=pan.read_csv(name, header=None, delimiter='\t',skiprows=2)
        self.PXRD={'2Theta':file[0],'Intensity':file[1]}
        #scale the intensity
        self.PXRD['Intensity']=self.PXRD['Intensity']/np.max(self.PXRD['Intensity'])
        
    def load_background(self,name): 
        file=pan.read_csv(name, header=None, delimiter='\t',skiprows=2)
        self.PXRD_bk={'2Theta':file[0],'Intensity':file[1]}
        #scale the intensity
        self.PXRD_bk['Intensity']=self.PXRD_bk['Intensity']/np.max(self.PXRD_bk['Intensity'])
        
    def plot_data(self,x,y,lb):
        self.dataplot1.axes.cla()
        self.dataplot1.axes.plot(x,y,label=lb)
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
        self.dataplot1.axes.plot(x,y,label=lb)
        self.dataplot1.axes.set_xlim(0,90)
        self.dataplot1.axes.set_ylim(-0.1,1.1)
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
        l4_button=QPushButton('Generate Data')
        l4_button.clicked.connect(lambda: self.create_testing_data())
        l4_button.clicked.connect(lambda: self.plot_data(self.PXRD['2Theta'],self.PXRD['Intensity'],'Raw data'))        
        l4_button.clicked.connect(lambda: self.update_plot(self.PXRD_bk['2Theta'],self.PXRD_bk['Intensity'],'Background') if self.check.isChecked() else print('no background file used'))
        l4_button.clicked.connect(lambda: self.update_plot(self.PXRD['2Theta'],self.PXRD['Intensity']-self.PXRD_bk['Intensity'],'Raw data minus background') if self.check.isChecked() else print('no background file used'))
        l4_button.clicked.connect(lambda: self.update_plot(self.PXRD_ML['2Theta'],self.PXRD_ML['Intensity'],'Testing data'))
        #adds widgets
        layout.addWidget(scale_text, 0,0) 
        layout.addWidget(self.scale_value, 1,0)
        layout.addWidget(bin_text, 0,1) 
        layout.addWidget(self.bin_text, 1,1)
        layout.addWidget(l4_button, 2,0,1,2)
        self.AnalysisGUI.setLayout(layout)
        
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
#%%
#This is the actual code to run the gui       
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
