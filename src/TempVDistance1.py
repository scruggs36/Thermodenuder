# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 13:11:04 2016

@author: austen
"""
#Rough Thermodenuder Measurements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FilePath='/home/austen/Documents/Thermodenuder/Data/Initial Tests/12-23-16/TempVDistance1.csv'
Data=pd.read_csv(FilePath,header=0,sep=',')
TempAverages=[]
TempSTDs=[]
for i in Data.index:
    AVGS=np.average([Data.loc[i,'0 Min Temperature (Celsius)'],Data.loc[i,'3 Min Temperature (Celsius)'],Data.loc[i,'5 Min Temperature (Celsius)']])
    STDs=np.std([Data.loc[i,'0 Min Temperature (Celsius)'],Data.loc[i,'3 Min Temperature (Celsius)'],Data.loc[i,'5 Min Temperature (Celsius)']])
    TempAverages.append(AVGS)
    TempSTDs.append(STDs)
TempAverages=pd.DataFrame(TempAverages)
TempSTDs=pd.DataFrame(TempSTDs)
TempAverages.columns=['Averaged Temperatures (Celsius)']
TempSTDs.columns=['STD Temperatures (Celsius)']
AVGSTDs=TempAverages.join(TempSTDs)
DATA=Data.join(AVGSTDs)

f, ax1=plt.subplots(1, figsize=(8,5))
ax1.errorbar(x=DATA.loc[:,'Distance Inside (Inches)'],y=DATA.loc[:,'Averaged Temperatures (Celsius)'],yerr=DATA.loc[:,'STD Temperatures (Celsius)'],fmt='go',label='Mean Temperature vs. Distance')
ax1.set_title('Mean of Measured Temperatures taken at 0, 3, and 5 Minutes as a Function of Distance Inside the Thermodenuder')
ax1.set_ylabel('Mean Temperature (C)')
ax1.set_xlabel('Distance Inside Thermodenuder (Inches)')
plt.legend(loc=2)
plt.show()