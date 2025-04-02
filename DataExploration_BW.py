#Brian West
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
import math

currentFolder = os.getcwd()
print(currentFolder)
terminalFiles = currentFolder + '/data/terminalUnits'
roofTopFiles = currentFolder + '/data/roofTopUnits'
cleanTerminalFiles = currentFolder +'/data/cleanTerminalUnits'

rawRTU1 = pd.read_csv('data/roofTopUnits/RTU_1.csv')
rawRTU2 = pd.read_csv('data/roofTopUnits/RTU_2.csv')
rawRTU3 = pd.read_csv('data/roofTopUnits/RTU_3.csv') # different columns? different type of unit


#forward fill set point
setPoint = 'Sp'
for filename in os.listdir(terminalFiles):
    fileData = pd.read_csv(os.path.join(terminalFiles,filename))
    for colName, colData in fileData.items():
        if setPoint in colName:
            fileData[colName] = fileData[colName].ffill()
    fileData.drop(columns = ['Air_Flow_Diff'])
    fileData.drop(columns = ['Room_Temperature_Diff'])
    fileData.drop(columns = ['VAV_Temperature_Diff'])
    fileData.to_csv(os.path.join(cleanTerminalFiles,filename))
    
            
# #merge all the files into one file
# terminalUnitsRawData = pd.DataFrame()
# for filename in os.listdir(terminalFiles):
#     terminalDesignation = (os.path.splitext(filename)[0])
#     fileData = pd.read_csv(os.path.join(terminalFiles,filename))
    
#     fileData.insert(0,'designation',terminalDesignation)                     
#     terminalUnitsRawData = pd.concat([terminalUnitsRawData,fileData])

# #per jeff's email
# terminalUnitsRawData.drop(columns = ['Air_Flow_Diff'])
# terminalUnitsRawData.drop(columns = ['Room_Temperature_Diff'])
# terminalUnitsRawData.drop(columns = ['VAV_Temperature_Diff'])

# terminalUnitsRawData.to_csv('data/terminalUnitsRawData.csv',index=False)


# #get basic stats on all columns
# file = open("data/terminalDescription.txt", "w")
# file.write("Total Rows\n")
# file.write(str(len(terminalUnitsRawData)))
# file.write("\n\n")

# for colName, data in terminalUnitsRawData.items():
#     file.write(colName)
#     file.write("\n")
#     file.write(data.describe().to_string())
#     file.write("\n\n")


#merge all the files into one file

rawRTU1 = pd.read_csv('data/roofTopUnits/RTU_1.csv')
rawRTU2 = pd.read_csv('data/roofTopUnits/RTU_2.csv')
rawRTU3 = pd.read_csv('data/roofTopUnits/RTU_3.csv') # different columns? different type of unit

timelessRTU1 = rawRTU1
timelessRTU1.drop(columns=['time'])
timelessRTU2 = rawRTU2
timelessRTU2.drop(columns=['time'])
timelessRTU3 = rawRTU3
timelessRTU3.drop(columns=['time'])


#approach find correlation between ALL RTU columns and ALL terminal unit columns (except time lol)
for filename in os.listdir(cleanTerminalFiles):
    fileData = pd.read_csv(os.path.join(cleanTerminalFiles,filename))
    fileData.drop(columns=['time'])
    corr1 = timelessRTU1.corrwith(fileData)
    corr2 = timelessRTU2.corrwith(fileData)
    corr3 = timelessRTU3.corrwith(fileData)
    corr1.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU1.csv')
    corr2.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU2.csv')
    corr3.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU3.csv')


#PCA requires data to be filled in
#clustering is worthless without having some summarized metric for each terminal unit. Maybe averaging values?

