# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:34:55 2017

@author: aks09000
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ntpath
import re
import glob
from scipy.optimize import curve_fit

#here we define the file path, and glob.glob finds the files in the file path we have set with the basename .txt
path="/home/austen/Documents/Thermodenuder/Data/Initial Tests/02-22-2017/*.txt"
files=glob.glob(path)

#So here is where python kinda works like C, it is easiest to declare every array ahead of time, then add to it later
d=pd.DataFrame()
Data={}
DataSummary={}
FileDirectories=[]
FileNames=[]
ParticleGeomMeanSize=[]
ParticleConcentration=[]
TimeStamps=[]


#This loop adds to the file directories and the file names to the empty arrays above
#in the future name all the files the same name and have the computer differentiate the files by unsing (#) eg. NewName (1).txt
#this will solve the ordering issues you see below after dataframe manipulation
for fle in files:
    FileDirectories.append(fle)
    FileNames.append(ntpath.basename(fle))
    
#Here is where we add our arrays to the empty dataframe we declared above
d['File Directories']=FileDirectories
d['File Names']=FileNames

#this is a quick way to read lines from a text file and select the line desired and put that line into an empty list    
for fle in files:
    f=open(fle, "r")
    for i, line in enumerate(f):
        if i== 147:
            SplitLine1=re.split(r'\t+',line.rstrip('\r\n'))
            ParticleGeomMeanSize.append(float(SplitLine1[1]))      
        if i == 150:
            SplitLine2=re.split(r'\t+',line.rstrip('\r\n'))
            ParticleConcentration.append(float(SplitLine2[1]))
            
#I am adding the arrays we read from the text files to the dataframe d           
d['Particle Size Geometric Mean']=ParticleGeomMeanSize
d['Total Particle Concentration (#/cc)']=ParticleConcentration

 
#The for loop below does a lot, lets try to break it down
# 1. it creates a dictionary and for each item in the dictionary a dataframe is assigned to that dictionary item
# 2. I made the index a column becasue the index was actually the size bin, then i reset the index numbering to be 0 to end rows
# 3. I create another dictionary, each item in the dictionary is assigned a dataframe which is composed of the summary in the text files given in just about the first 18 lines
# 4. I rename the column names of each dataframe in the dictionary
# 5. I append parameter values I want from row 16 of the dataframes of each dictionary item to an empty list
for i in d.index:
    Data["T{}".format(i)]=pd.read_csv(d.loc[i,'File Directories'], delimiter='\t',skiprows=18, nrows=107, error_bad_lines=False)
    Data["T{}".format(i)]['Size Bin']=Data["T{}".format(i)].index
    Data["T{}".format(i)]=Data["T{}".format(i)].reset_index(drop=True)
    Data["T"+str(i)].columns=['dw/dLogDP','Size Bin']
    DataSummary["S{}".format(i)]=pd.read_csv(d.loc[i,'File Directories'], delimiter='\t', nrows=18, error_bad_lines=False)
    DataSummary["S"+str(i)].columns=['Parameter','Parameter Value']
    TimeStamps.append(DataSummary['S'+str(i)].loc[16,'Parameter Value'])

#Here we add the time the samples were taken into the dataframe as an array of strings
d['Time Stamp']=TimeStamps

#This is a function we wrote to plot all the distributions we acquired
def PlotAllDistributions(DF):
    for i in DF.index:   
        plt.bar(Data['T'+str(i)].loc[:,'Size Bin'],Data['T'+str(i)].loc[:,'dw/dLogDP'])
        plt.xlabel('Particle Diameter (nm)')
        plt.ylabel('dw/dLogDP')
        plt.title(d.loc[i,'File Directories'][-8:]+' Particle Size Distribution')
        plt.show()
    return

#here I need to  add the information about thermodenuder set temperatures from my lab note that corresopnd to the file names given in the dataframe directory  
#there are 15 files we took so the array needs to be 15 elements long, I could do this later but whatever we are doing this now 
#d['Thermodenuder Temperature']=[100.0,np.NaN,150.0,np.NaN,np.NaN,50.0,25.0,np.NaN,np.NaN,200.0,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN] 

        
#We need to sort datafame d by dropping experiments that did not use the thermodenuder
#datafreme.drop the axis parameters specify whether rows or columns are being dropped axis=0 for dropping rows, axis=1 for dropping columns
#This function actually operates on the dataframe being used, so create a copy of the dataframe and then operate on the copy to get a new dataframe (the new dataframe takes the name of the copy)
#notice that the drop function when dropping rows acts on the dataframe given so there is no need to do df=df.drop(etc...)
def DropFilesFromDF(DF,DropFileNames):
    copy=DF.copy()
    DropArray=[]
    for dropindex, FileName in enumerate(copy['File Names']):
        for DropFileName in DropFileNames:
            if FileName==DropFileName:
                DropArray.append(dropindex)
    copy.drop(DropArray, axis=0, inplace=True)
    copy=copy.reset_index(drop=True)
    return copy

#I put the function we just made to work here, creating a dataframe where only the files that use the TD are present    
FilesToDrop1=['T001.txt','T002.txt','T003.txt','T004.txt','T006.txt','T011.txt','T012.txt','T013.txt','T014.txt','T015.txt']
TDDF=DropFilesFromDF(d,FilesToDrop1)
TDDF['Thermodenuder Temperature']=[100.0,150.0,50.0,20.0,200.0]
#Here i change the order of the files to match the ascending order of the temperatures, then I reset the index of the dataframe
TDDF=TDDF.sort(columns=['Thermodenuder Temperature'], axis=0, ascending=True)
TDDF=TDDF.reset_index(drop=True)
#Here I create a dataframe composed of files that were only ambient background files
FilesToDrop2=['T001.txt','T002.txt','T003.txt','T004.txt','T005.txt','T007.txt','T008.txt','T009.txt','T010.txt','T012.txt','T013.txt']
BackgroundDF=DropFilesFromDF(d,FilesToDrop2)
#We will average the ambient (no thermodenuder used) particle concentrations from all the text files here, we made an array of constants out of the average
AmbientAvgGeoMean=np.full((5,1),np.mean(BackgroundDF['Particle Size Geometric Mean']))
AmbientAvgConc=np.full((5,1),np.mean(BackgroundDF['Total Particle Concentration (#/cc)']))
#define a function for the fitting
def Quadratic(x,A,B,C):
    return((A*x**2)+B*x+C)
def Linear(x,a,b):
    return
#conduct the curve fitting
popt, pcov=curve_fit(Quadratic,TDDF['Thermodenuder Temperature'],TDDF['Particle Size Geometric Mean'])
equation='y='+str(popt[0])+'x**2+'+str(popt[1])+'x+'+str(popt[2])
#from thermodenuder dataframe we will plot Geometric Mean Particle Size vs. Thermodenuder Temperature
f, ax=plt.subplots(figsize=(10,10))
ax.plot(TDDF['Thermodenuder Temperature'],TDDF['Particle Size Geometric Mean'], 'bo', label='Particle Size vs. Celsius')
ax.plot(TDDF['Thermodenuder Temperature'],AmbientAvgGeoMean,'r--', label='Ambient Particle Size Geometric Mean')
ax.plot(TDDF['Thermodenuder Temperature'],Quadratic(TDDF['Thermodenuder Temperature'],popt[0],popt[1],popt[2]),'y--',label='Particle Size vs. Celsius Fit')
ax.set_ylabel('Particle Size Geometric Mean (nm)')
ax.set_xlabel('Thermodenuder Temperature (C)')
ax.set_title('Particle Size Geometric Mean as a Function of Thermodenuder Wall Temperature')
ax.legend(bbox_to_anchor=(1.85,1))
ax.text(70,70,equation)
plt.show()
#we will plot the concentration vs thermodenuder temperature here, and mark the average ambient concentration on the plot, and fit the curve, and calculate transmission efficiency as a function of temperature and make that another plot with its own fit
f, ax1=plt.subplots(figsize=(10,10))
ax1.plot(TDDF['Thermodenuder Temperature'],TDDF['Total Particle Concentration (#/cc)'], 'bo--', label='Particle Conc. vs. Celsius')
ax1.plot(TDDF['Thermodenuder Temperature'],AmbientAvgConc, 'r--', label='Average Ambient Particle Conc')
ax1.set_ylabel('Particle Concentration (#/cc)')
ax1.set_xlabel('Thermodenuder Temperature (C)')
ax1.set_title('Particle Concentration as a Function of Thermodenuder Wall Temperature')
ax1.legend(bbox_to_anchor=(1.85,1))
plt.show()