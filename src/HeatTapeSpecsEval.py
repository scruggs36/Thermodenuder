# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 13:57:14 2016

@author: austen
"""
#Thermodenuder Heat Tape Coverage Calculations
#Import packages
import math as math
import pandas as pd

#Import heat tape specifications file
FilePath='/home/austen/Documents/Thermodenuder/Data/Initial Tests/12-20-16/OmegaHeatTapes.csv'
HeatTapeSpecs=pd.read_csv(FilePath,header=0,sep=',')

#Define constants for calculations
PipeLength=1000.00
PipeDiameter=0.5*2.54*10
LengthPerCoil=2*math.pi*(PipeDiameter/2)

#Write function to output calculations
def Equations(HeatTapeModel,TapeLength, TapeWidth, Gap, Voltage, Cost):
    MaxNumCoils=(TapeLength*12.0*2.54*10)/LengthPerCoil
    NumCoilsRequired=PipeLength/((TapeWidth*2.54*10)+Gap)
    MinCoilSpanwGap=PipeLength/MaxNumCoils
    CoilSpanwGap=PipeLength/NumCoilsRequired
    RequiredLessThanMax=MaxNumCoils>=NumCoilsRequired
    CalculationOutput=pd.Series(data={'Model':HeatTapeModel,'Cost (USD)':Cost,'Volts':Voltage,'Tape Length (Feet)':TapeLength,'Tape Width (Inches)':TapeWidth,'Max Coil #':MaxNumCoils,'Required Coil #':NumCoilsRequired,'Minimum Pipe Length Per Coil':MinCoilSpanwGap,'Nominal Pipe Length Per Coil (Gap Included)':CoilSpanwGap,'Nominal Less Than Maximum Coils':RequiredLessThanMax})
    CalculationOutput=pd.DataFrame(CalculationOutput).T
    return(CalculationOutput)
    
#Perform calulations via looping over rows in the file
Results=pd.DataFrame()
for i in range(len(HeatTapeSpecs.index)):
    OutputArray=Equations(HeatTapeModel=HeatTapeSpecs.loc[i,'Heat Tape Model Number'],Voltage=HeatTapeSpecs.loc[i,'Volts'],Cost=HeatTapeSpecs.loc[i,'Cost (USD)'],TapeLength=HeatTapeSpecs.loc[i,'Length (Feet)'],TapeWidth=HeatTapeSpecs.loc[i,'Width (Inches)'],Gap=5.0)
#   must be results=results.append(blah) to store the looped over data
#   ignore index is important, it basically returns the index as the row number of the particular dataframe you made
    Results=Results.append(OutputArray, ignore_index=True)
#This is the proper way to sort through a data frame and drop rows
for index, row in Results.iterrows():
    if row['Nominal Less Than Maximum Coils']==False:
        Results.drop(index, inplace=True)
for index, row in Results.iterrows():
    if row['Volts']==240:
        Results.drop(index, inplace=True)
csv_filepath='/home/austen/Documents/Thermodenuder/CompatibleOmegaHeatTapes.csv'
Results.to_csv(csv_filepath, sep=',')