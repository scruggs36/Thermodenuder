# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 13:11:04 2016

@author: austen
"""
#Rough Thermodenuder CPC Measurements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

FilePath1='/home/PycharmProjects/Thermodenuder/Data/CPC & DMA/02-22-2017/TD0001.txt'
FilePath2='/home/austen/Documents/Thermodenuder/Data/Initial Tests/01-11-17/TD0002.txt'
FilePath3='/home/austen/Documents/Thermodenuder/Data/Initial Tests/01-11-17/TD0003.txt'
FilePath4='/home/austen/Documents/Thermodenuder/Data/Initial Tests/01-11-17/TD0004.txt'
TD0001=pd.read_csv(FilePath1,header=None,sep=',')
TD0002=pd.read_csv(FilePath2,header=None,sep=',')
TD0003=pd.read_csv(FilePath3,header=None,sep=',')
TD0004=pd.read_csv(FilePath4,header=None,sep=',')

#Name Column Headers
TD0001.columns=["Time Stamp","Particles/CC"]
TD0002.columns=["Time Stamp","Particles/CC"]
TD0003.columns=["Time Stamp","Particles/CC"]
TD0004.columns=["Time Stamp","Particles/CC"]
    
SecondsElapsed1=[]
SecondsElapsed2=[]
SecondsElapsed3=[]
SecondsElapsed4=[]

#These for loops subtract the first time point from all subsequent points taken
#in time and append the seconds elapsed since the first time point to the seconds
#elapsed array, this array is then added to a new column in the data frame we imported origionally
for elem in TD0001.index:
    DeltaT1=(datetime.strptime(TD0001.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0001.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed1.append(DeltaT1)
TD0001['Seconds']=pd.Series(SecondsElapsed1, index=TD0001.index)
for elem in TD0002.index:
    DeltaT2=(datetime.strptime(TD0002.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0002.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed2.append(DeltaT2)
TD0002['Seconds']=pd.Series(SecondsElapsed2, index=TD0002.index)
for elem in TD0003.index:
    DeltaT3=(datetime.strptime(TD0003.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0003.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed3.append(DeltaT3)
TD0003['Seconds']=pd.Series(SecondsElapsed3, index=TD0003.index)
for elem in TD0004.index:
    DeltaT4=(datetime.strptime(TD0004.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0004.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed4.append(DeltaT4)
TD0004['Seconds']=pd.Series(SecondsElapsed4, index=TD0004.index)
TD0004.drop(TD0004.index[[np.arange(1000,len(TD0004.index),1)]], inplace=True)
    
f, ax1=plt.subplots(1, figsize=(10,10))
ax1.plot(TD0001.loc[:,'Seconds'],TD0001.loc[:,"Particles/CC"],'g-',label="Particles/CC vs. Seconds (Pre-TD)")
ax1.plot(TD0002.loc[:,'Seconds'],TD0002.loc[:,"Particles/CC"],'b-',label="Particles/CC vs. Time (TD OFF)")
ax1.plot(TD0003.loc[:,'Seconds'],TD0003.loc[:,"Particles/CC"],'r-',label="Particles/CC vs. Time (TD ON)")
ax1.plot(TD0004.loc[:,'Seconds'],TD0004.loc[:,"Particles/CC"],'y-',label="Particles/CC vs. Time (TD After Meas.)")
ax1.set_title('Impact on CPC Measurements Before, During, and After Heating via Thermodenuder')
ax1.set_ylabel('Particles/CC')
ax1.set_xlabel('Time (Seconds)')
ax1.annotate('Signal too high upon heating, so I watched it decay down while cooling.', xy=(200, 2000000), xytext=(400, 2000000), arrowprops=dict(facecolor='black', shrink=0.05))
plt.legend(loc=2)
plt.show()  

f, ax2=plt.subplots(1, figsize=(10,10))
ax2.plot(TD0001.loc[:,'Seconds'],TD0001.loc[:,"Particles/CC"],'g-',label="Particles/CC vs. Seconds (Pre-TD)")
ax2.plot(TD0002.loc[:,'Seconds'],TD0002.loc[:,"Particles/CC"],'b-',label="Particles/CC vs. Time (TD OFF)")
ax2.plot(TD0004.loc[:,'Seconds'],TD0004.loc[:,"Particles/CC"],'y-',label="Particles/CC vs. Time (TD After Meas.)")
ax2.set_title('Impact on CPC Measurements Before, During, and After Heating via Thermodenuder')
ax2.set_ylabel('Particles/CC')
ax2.set_xlabel('Time (Seconds)')
plt.legend(loc=2)
plt.show()   
   

