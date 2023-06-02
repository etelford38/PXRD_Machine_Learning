# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 17:23:00 2023

@author: Evan Telford (ejt2133@columbia.edu)
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mt
import string
#%%
def create_figure(rows,columns,height,wspace,hspace,resolution,letters):
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 6}
    mt.rc('font', **font)
    mt.rcParams['pdf.fonttype'] = 42
    mt.rcParams['ps.fonttype'] = 42
    mt.rcParams['font.family'] = 'Arial'
    fig, axes = plt.subplots(nrows=rows,ncols=columns,figsize=(7,height),gridspec_kw={'wspace':wspace,'hspace':hspace},dpi=resolution)
    plt.rcParams['text.color'] = 'k'
    plt.rcParams['axes.labelcolor'] = 'k'
    plt.rcParams['xtick.color'] = 'k'
    plt.rcParams['ytick.color'] = 'k'

    axes=np.reshape(axes,(1,np.size(axes)))[0]

    for i,f in enumerate(axes):
        ax=f
        ax.spines['left'].set_color('k')
        ax.spines['right'].set_color('k')
        ax.spines['bottom'].set_color('k')
        ax.spines['top'].set_color('k')
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['right'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['top'].set_linewidth(0.5)
        ax.tick_params(width=0.5,length=2.0)
        # ax.axis('off')
        if letters==True:
            f.text(-0.2, 1.02, string.ascii_uppercase[i], transform=f.transAxes, 
                size=12, weight='bold')
        else:
            pass
    return fig, axes

def create_figure_mosaic(mosaicity,height,wspace,hspace,resolution,letters):
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 6}
    mt.rc('font', **font)
    mt.rcParams['pdf.fonttype'] = 42
    mt.rcParams['ps.fonttype'] = 42
    mt.rcParams['font.family'] = 'Arial'
    fig, axes = plt.subplot_mosaic(mosaicity,figsize=(7,height),gridspec_kw={'wspace':wspace,'hspace':hspace},dpi=resolution)
    plt.rcParams['text.color'] = 'k'
    plt.rcParams['axes.labelcolor'] = 'k'
    plt.rcParams['xtick.color'] = 'k'
    plt.rcParams['ytick.color'] = 'k'

    for label, ax in axes.items():
        ax.spines['left'].set_color('k')
        ax.spines['right'].set_color('k')
        ax.spines['bottom'].set_color('k')
        ax.spines['top'].set_color('k')
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['right'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['top'].set_linewidth(0.5)
        ax.tick_params(width=0.5,length=2.0)
        # ax.axis('off')
        if letters==True:
            ax.text(-0.2, 1.02, label, transform=ax.transAxes, 
                size=12, weight='bold')
        else:
            pass
    return fig, axes
        
def create_single_axis_subplot(figure,axes,xlabel,ylabel,title):
    axes.tick_params(direction="in")
    axes.yaxis.set_ticks_position(position='both')
    axes.xaxis.set_ticks_position(position='both')
    axes.set_xlabel(xlabel, labelpad=0.1)
    axes.set_ylabel(ylabel, labelpad=0.1)
    axes.set_title(title,fontsize=8,pad=3)
    
def create_image_subplot(figure,axes,title):
    axes.tick_params(direction="in")
    axes.yaxis.set_ticks_position(position='both')
    axes.xaxis.set_ticks_position(position='both')
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_title(title,fontsize=8,pad=3)
    
def create_double_axis_subplot(figure,axes,xlabel,ylabel1,ylabel2,title,axcolor1,axcolor2):
    f=axes  
    f.set_xlabel(xlabel,labelpad=0.0)
    f.set_ylabel(ylabel1,labelpad=0.0)
    f.set_title(title,fontsize=8,pad=3)
    f.patch.set_visible(False)
    f.tick_params(direction="in")
    f.xaxis.set_ticks_position(position='both')
    
    g=f.twinx()
    g.spines['left'].set_color('k')
    g.spines['right'].set_color('k')
    g.spines['bottom'].set_color('k')
    g.spines['top'].set_color('k')
    g.spines['left'].set_linewidth(0.5)
    g.spines['right'].set_linewidth(0.5)
    g.spines['bottom'].set_linewidth(0.5)
    g.spines['top'].set_linewidth(0.5)
    g.tick_params(width=0.5,length=2.0)
    g.set_ylabel(ylabel2,labelpad=0.0)  
    g.tick_params(direction="in")
    
    g.set_zorder(0)
    f.set_zorder(1) 
    
    f.yaxis.label.set_color(axcolor1)
    g.yaxis.label.set_color(axcolor2)
    f.tick_params(axis='y',colors=axcolor1)
    g.tick_params(axis='y',colors=axcolor2)
    f.spines['left'].set_color(axcolor1)
    f.spines['right'].set_color(axcolor2)
    
    return f,g
    
def save_plot(title):
    plt.savefig(title, bbox_inches='tight', dpi=600, pad_inches = 0)   
