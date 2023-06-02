# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:42:12 2023

@author: Evan Telford (ejt2133@columbia.edu)
"""
#%%
#import libraries to load
from mp_api.client import MPRester
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import numpy as np
import pickle
from scipy.special import wofz
from scipy.interpolate import CubicSpline
import Figure_making_functions as FIG
#%%
#define functions
def generate_PXRD(mpid):
    with MPRester(api_key="zRp6l2Rom2MHPIErj8WG1rgkVIAdbp9m") as mpr:
        # first retrieve the relevant structure
        structure = mpr.get_structure_by_material_id(mpid)
    # important to use the conventional structure to ensure
    # that peaks are labelled with the conventional Miller indices
    sga = SpacegroupAnalyzer(structure)
    conventional_structure = sga.get_conventional_standard_structure()
    # this example shows how to obtain an XRD diffraction pattern
    # these patterns are calculated on-the-fly from the structure
    calculator = XRDCalculator(wavelength="CuKa")
    pattern = calculator.get_pattern(conventional_structure)
    
    return pattern
    
def generate_spline(x,y):
    spl = CubicSpline(x, y)
    
    return spl

def voigt(x, x0, sigma, gamma):
    """Voigt lineshape function."""
    z = ((x - x0) + 1j * gamma) / (sigma * np.sqrt(2))
    
    return np.real(wofz(z).real) / (sigma * np.sqrt(2 * np.pi))

def generate_PXRD_voigt(T, peaks, sigma, gamma,num):
    """Generate PXRD data from a list of peaks using Voigt lineshapes."""
    x = np.linspace(0,90, num)
    y = np.zeros_like(x)
    for i,peak in enumerate(peaks):
        x0 = T[i] 
        intensity = peak
        y += intensity * voigt(x, x0, sigma, gamma)

    return x, y

def generate_PXRD_plot(mpid):
    #generate PXRD data from Materials API
    pt=generate_PXRD(mpid)
    #generate figure and axis data
    fig,axes=FIG.create_figure(1,1,5,0,0,600,False)
    FIG.create_single_axis_subplot(figure=fig, axes=axes[0], xlabel=pt.XLABEL, ylabel=pt.YLABEL, title=mpid)
    axes[0].set_ylim(-5,150)
    #plot the raw PXRD peaks
    axes[0].plot(pt.x,pt.y,'k+',label='generated peaks')
    #create spline fit
    sp=generate_spline(pt.x, pt.y)
    sp_x=np.linspace(np.min(pt.x),np.max(pt.x),501)
    #plot the spline
    axes[0].plot(sp_x,sp(sp_x),'r-.',linewidth=0.5,label='spline fit')
    #generate voigt fit
    sigma=0.2
    gamma=0.1
    x_v,y_v=generate_PXRD_voigt(pt.x,pt.y,sigma,gamma,1000)
    #plot the voigt fit
    axes[0].plot(x_v,y_v,'b--',linewidth=0.5,label='Voigt fit')
    #additional plot points
    axes[0].legend(fontsize=6,loc='upper right')
    axes[0].set_xlim(0,90)

def generate_PXRD_data(pt,num):
    #generate voigt fit
    sigma=0.2
    gamma=0.1
    x_v,y_v=generate_PXRD_voigt(pt.x,pt.y,sigma,gamma,num)
    
    return x_v, y_v
    
def return_MD(elements):
    # Step 1: Set up the API key
    api_key = "zRp6l2Rom2MHPIErj8WG1rgkVIAdbp9m"
    # Step 2: Initialize MPRester with your API key
    mpr = MPRester(api_key)
    # Step 3: Query the Materials Project for XRD data and structure class
    data = mpr.summary.search(elements=elements,fields=["material_id", "structure","elements","composition_reduced","formula_pretty","symmetry"])
    
    return data

def create_MD_dictionary(elements):
    #access the database to generate information
    data=return_MD(elements)
    #create the final dictionary
    data_dic={}
    #loop through all compiled materials and add the information to the dictionary
    for crystals in data:
        #find the material id
        id=crystals.material_id
        #determine the diffraction pattner
        pattern=generate_PXRD(id)
        data_dic[id]={'data':crystals, 'PXRD':pattern}
    
    return data_dic

def create_MD_dictionary_reduced(elements):
    #access the database to generate information
    data=return_MD(elements)
    #create the final dictionary
    data_dic={}
    #loop through all compiled materials and add the information to the dictionary
    for crystals in data:
        #find the material id
        iden=crystals.material_id
        structure=crystals.structure
        symm=crystals.symmetry
        elements=crystals.elements
        #determine the diffraction pattner
        pattern=generate_PXRD(iden)
        data_dic[iden]={'structure':structure,'symmetry':symm,'elements':elements,'PXRD':pattern}
    
    return data_dic

def save_dictionary(dic,name):
    with open(name+'.pkl', 'wb') as file:
        pickle.dump(dic, file)
        
def open_dictionary(name):
    with open(name+'.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    
    return loaded_data

def generate_MP_dataset(elements,name):
    data=create_MD_dictionary_reduced(elements)
    save_dictionary(data,name)
