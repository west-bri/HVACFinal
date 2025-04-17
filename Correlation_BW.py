import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
import math
import seaborn as sns
from collections import defaultdict
import csv
from sklearn.cluster import KMeans

#Get timestamps from clean Terminal Units
#correlate between each RTU and TU



# use cleanTerminalUnits for correlations
currentFolder = os.getcwd()
cleanTerminalFiles = currentFolder +'/data/cleanTerminalUnits'

rawRTU1 = pd.read_csv('data/roofTopUnits/RTU_1.csv',index_col='time')
rawRTU2 = pd.read_csv('data/roofTopUnits/RTU_2.csv',index_col='time')
rawRTU3 = pd.read_csv('data/roofTopUnits/RTU_3.csv',index_col='time')

setPoint = 'Sp'

for colName in rawRTU1:
    if setPoint in colName:
        rawRTU1[colName] = rawRTU1[colName].ffill()

for colName in rawRTU2:
    if setPoint in colName:
        rawRTU2[colName] = rawRTU2[colName].ffill()

for colName in rawRTU1:
    if setPoint in colName:
        rawRTU2[colName] = rawRTU2[colName].ffill()


cleanRTU1 = rawRTU1
cleanRTU1.drop(columns=['ClgStgCmd02'],inplace=True)
cleanRTU1.drop(columns=['EconEna'],inplace=True)
cleanRTU1.drop(columns=['EconEnaSp'],inplace=True)
cleanRTU1.drop(columns=['EffRmSp'],inplace=True)
cleanRTU1.drop(columns=['ExhAirDmprFbk'],inplace=True)
cleanRTU1.drop(columns=['FltAlm'],inplace=True)
cleanRTU1.drop(columns=['HtgAlm'],inplace=True)
cleanRTU1.drop(columns=['HtgPct'],inplace=True)
cleanRTU1.drop(columns=['HtgStgCmd01'],inplace=True)
cleanRTU1.drop(columns=['HtgStgCmd02'],inplace=True)
cleanRTU1.drop(columns=['OccCmd'],inplace=True)
cleanRTU1.drop(columns=['OccStatus'],inplace=True)
cleanRTU1.drop(columns=['SuplAirHtgSp'],inplace=True)
cleanRTU1.drop(columns=['SuplAirTempAlm'],inplace=True)
cleanRTU1.drop(columns=['SuplAirTempSp'],inplace=True)
cleanRTU1.drop(columns=['SuplFanAlm'],inplace=True)
cleanRTU1.drop(columns=['UnoccHtgSp'],inplace=True)
cleanRTU1.drop(columns=['oppMode'],inplace=True)
cleanRTU1.dropna(inplace=True)
cleanRTU1.drop(columns=['ExhFanStatus'], inplace=True) # not in other RTU
cleanRTU1.columns = cleanRTU1.columns.values + "RTU1" #add suffixes to make handling columns consistent

cleanRTU2 = rawRTU2
cleanRTU2.drop(columns=['ClgStgCmd02'],inplace=True)
cleanRTU2.drop(columns=['EconEna'],inplace=True)
cleanRTU2.drop(columns=['EconEnaSp'],inplace=True)
cleanRTU2.drop(columns=['EffRmSp'],inplace=True)
cleanRTU2.drop(columns=['ExhAirDmprFbk'],inplace=True)
cleanRTU2.drop(columns=['FltAlm'],inplace=True)
cleanRTU2.drop(columns=['HtgAlm'],inplace=True)
cleanRTU2.drop(columns=['HtgPct'],inplace=True)
cleanRTU2.drop(columns=['HtgStgCmd01'],inplace=True)
cleanRTU2.drop(columns=['HtgStgCmd02'],inplace=True)
cleanRTU2.drop(columns=['OccCmd'],inplace=True)
cleanRTU2.drop(columns=['OccStatus'],inplace=True)
cleanRTU2.drop(columns=['SuplAirHtgSp'],inplace=True)
cleanRTU2.drop(columns=['SuplAirTempAlm'],inplace=True)
cleanRTU2.drop(columns=['SuplAirTempSp'],inplace=True)
cleanRTU2.drop(columns=['SuplFanAlm'],inplace=True)
cleanRTU2.drop(columns=['UnoccHtgSp'],inplace=True)
cleanRTU2.drop(columns=['oppMode'],inplace=True)
cleanRTU2.dropna(inplace=True)
cleanRTU2.columns = cleanRTU2.columns.values + "RTU2"
cleanRTU3 = rawRTU3
cleanRTU3.dropna(inplace=True)
cleanRTU3.columns = cleanRTU3.columns.values + "RTU3"

cleanRTU1.to_csv('data/roofTopUnits/cleanRTU1.csv')
cleanRTU2.to_csv('data/roofTopUnits/cleanRTU2.csv')
cleanRTU3.to_csv('data/roofTopUnits/cleanRTU3.csv')

sorted_tu_files = sorted(os.listdir(cleanTerminalFiles))

for filename in sorted_tu_files:
    correlationDF = pd.DataFrame(columns=['variables','RTU1Corr','RTU2Corr'])
    fileData = pd.read_csv(os.path.join(cleanTerminalFiles,filename),index_col='time')
    fileData = fileData.iloc[:, 1:]
    fileDataRTU1 = pd.merge(fileData,cleanRTU1,on='time',how='inner') # merge on timestamps
    fileDataRTU1.dropna(inplace=True)
    fileDataRTU2 = pd.merge(fileData,cleanRTU2,on='time',how='inner')
    fileDataRTU2.dropna(inplace=True)
    #correlate each column of TU data to each column of each RTU
    for colNameTU, colDataTU in fileData.items():
        for colNameRTU1, colDataRTU1 in cleanRTU1.items():
            colNameRTU2 = colNameRTU1.replace("RTU1","RTU2")
            corr1 = fileDataRTU1[colNameTU].corr(fileDataRTU1[colNameRTU1])
            corr2 = fileDataRTU2[colNameTU].corr(fileDataRTU2[colNameRTU2])
            variables = colNameTU + "," + colNameRTU1
            newRow = pd.DataFrame([{'variables': variables, 'RTU1Corr': corr1, 'RTU2Corr': corr2}])
            correlationDF = pd.concat([correlationDF,newRow],ignore_index= False)
    correlationDF.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}.csv')

# for filename in sorted_tu_files:
#      fileData = pd.read_csv(os.path.join(cleanTerminalFiles,filename),index_col='time') # TU file
#      corr1 = fileData.corrwith(cleanRTU1,drop=True,numeric_only=True)
#      corr2 = fileData.corrwith(cleanRTU2,drop=True,numeric_only=True)
#      corr3 = fileData.corrwith(cleanRTU3,drop=True,numeric_only=True)
#      corr1.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU1.csv')
#      corr2.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU2.csv')
#      corr3.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU3.csv')
