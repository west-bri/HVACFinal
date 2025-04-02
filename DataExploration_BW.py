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
roofTopFiles = currentFolder + 'data/roofTopUnits'

#merge all the files into one file



setPoint = 'Sp'
terminalUnitsRawData = pd.DataFrame()
for filename in os.listdir(terminalFiles):
    terminalDesignation = (os.path.splitext(filename)[0])
    fileData = pd.read_csv(os.path.join(terminalFiles,filename))
    for colName, colData in fileData.items():
        if setPoint in colName:
            fileData[colName] = fileData[colName].ffill()
    fileData.insert(0,'designation',terminalDesignation)                     
    terminalUnitsRawData = pd.concat([terminalUnitsRawData,fileData])

#per jeff's email
terminalUnitsRawData.drop(columns = ['Air_Flow_Diff'])
terminalUnitsRawData.drop(columns = ['Room_Temperature_Diff'])
terminalUnitsRawData.drop(columns = ['VAV_Temperature_Diff'])

terminalUnitsRawData.to_csv('data/terminalUnitsRawData.csv',index=False)

terminalUnitsCleaned = terminalUnitsRawData.dropna()
terminalUnitsCleaned.to_csv('data/terminalUnitsCleaned.csv',index=False)

#get basic stats on all columns
file = open("data/terminalDescription.txt", "w")
file.write("Total Rows\n")
file.write(str(len(terminalUnitsRawData)))
file.write("\n\n")

for colName, data in terminalUnitsRawData.items():
    file.write(colName)
    file.write("\n")
    file.write(data.describe().to_string())
    file.write("\n\n")


#per email, setpoints can forward filled


# terminalScaleData = StandardScaler().fit_transform(terminalUnitsRawData.iloc[:,2:])
# pca = PCA(n_components = 28)
# pc = pca.fit(terminalScaleData)
# print(pc.explained_variance_ratio_)
# print(pc.components_)



# #prune data that does not change
# terminalPruned = terminalUnitsRawData
# terminalPruned['EffOcc'].drop() # occurs 206278 times with value of 0
# terminalPruned['OccCmd'].drop() # occurs 214773 times with value of 0
# terminalPruned['oppMode'].drop() # occurs 211455.0 times with value of 0
# terminalPruned['SuplFanCmd'].drop() # occurs 41121.0 times with value of 1
# terminalPruned['Heating_Stg_Cmd'].drop() # occurs 26292.0 times with value 2
# terminalPruned['SuplFanState'].drop() #occurs 2853 times with value -1

# terminalPruned.to_csv('data/terminalUnitsPruned.csv',index = False)


