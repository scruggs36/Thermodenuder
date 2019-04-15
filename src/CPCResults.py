# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 17:29:18 2017

@author: austen
"""

#Rough Thermodenuder CPC Measurements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

FilePath1='/home/austen/Documents/Thermodenuder/Data/Initial Tests/01-19-17/TD0005.txt'
FilePath2='/home/austen/Documents/Thermodenuder/Data/Initial Tests/01-19-17/TD0006.txt'
FilePath3='/home/austen/Documents/Thermodenuder/Data/Initial Tests/01-19-17/TD0007.txt'
FilePath4='/home/austen/Documents/Thermodenuder/Data/Initial Tests/01-19-17/TD0008.txt'
TD0005=pd.read_csv(FilePath1,header=None,sep=',')
TD0006=pd.read_csv(FilePath2,header=None,sep=',')
TD0007=pd.read_csv(FilePath3,header=None,sep=',')
TD0008=pd.read_csv(FilePath4,header=None,sep=',')

#Name Column Headers
TD0005.columns=["Time Stamp","Particles/CC"]
TD0006.columns=["Time Stamp","Particles/CC"]
TD0007.columns=["Time Stamp","Particles/CC"]
TD0008.columns=["Time Stamp","Particles/CC"]
    
SecondsElapsed1=[]
SecondsElapsed2=[]
SecondsElapsed3=[]
SecondsElapsed4=[]

#These for loops subtract the first time point from all subsequent points taken
#in time and append the seconds elapsed since the first time point to the seconds
#elapsed array, this array is then added to a new column in the data frame we imported origionally
for elem in TD0005.index:
    DeltaT1=(datetime.strptime(TD0005.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0005.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed1.append(DeltaT1)
TD0005['Seconds']=pd.Series(SecondsElapsed1, index=TD0005.index)
for elem in TD0006.index:
    DeltaT2=(datetime.strptime(TD0006.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0006.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed2.append(DeltaT2)
TD0006['Seconds']=pd.Series(SecondsElapsed2, index=TD0006.index)
for elem in TD0007.index:
    DeltaT3=(datetime.strptime(TD0007.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0007.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed3.append(DeltaT3)
TD0007['Seconds']=pd.Series(SecondsElapsed3, index=TD0007.index)
for elem in TD0008.index:
    DeltaT4=(datetime.strptime(TD0008.loc[elem,"Time Stamp"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(TD0008.loc[0,"Time Stamp"],"%Y-%m-%d %H:%M:%S")).seconds
    SecondsElapsed4.append(DeltaT4)
TD0008['Seconds']=pd.Series(SecondsElapsed4, index=TD0008.index)
#TD0004.drop(TD0004.index[[np.arange(1000,len(TD0004.index),1)]], inplace=True)
    
f, ax1=plt.subplots(1, figsize=(5,5))
ax1.plot(TD0005.loc[:,'Seconds'],TD0005.loc[:,"Particles/CC"],'g-',label="Particles/CC vs. Seconds (Pre-TD)")
ax1.plot(TD0006.loc[:,'Seconds'],TD0006.loc[:,"Particles/CC"],'b-',label="Particles/CC vs. Time (TD OFF)")
ax1.plot(TD0007.loc[:,'Seconds'],TD0007.loc[:,"Particles/CC"],'r-',label="Particles/CC vs. Time (TD ON)")
ax1.plot(TD0008.loc[:,'Seconds'],TD0008.loc[:,"Particles/CC"],'y-',label="Particles/CC vs. Time (Pre-TD After Meas.)")
ax1.set_title('Impact on CPC Measurements Before, During, and After Heating via Thermodenuder')
ax1.set_ylabel('Particles/CC')
ax1.set_xlabel('Time (Seconds)')
ax1.annotate('Signal too high upon heating, so I watched it decay down while cooling.', xy=(200, 2000000), xytext=(400, 2000000), arrowprops=dict(facecolor='black', shrink=0.05))
plt.legend(loc=2)
 

f, ax2=plt.subplots(1, figsize=(5,5))
ax2.plot(TD0005.loc[:,'Seconds'],TD0005.loc[:,"Particles/CC"],'g-',label="Particles/CC vs. Seconds (Pre-TD)")
ax2.plot(TD0006.loc[:,'Seconds'],TD0006.loc[:,"Particles/CC"],'b-',label="Particles/CC vs. Time (TD OFF)")
ax2.plot(TD0008.loc[:,'Seconds'],TD0008.loc[:,"Particles/CC"],'y-',label="Particles/CC vs. Time (Pre-TD After Meas.)")
ax2.set_title('Impact on CPC Measurements Before, During, and After Heating via Thermodenuder')
ax2.set_ylabel('Particles/CC')
ax2.set_xlabel('Time (Seconds)')
plt.legend(loc=2)
plt.show()   
   

