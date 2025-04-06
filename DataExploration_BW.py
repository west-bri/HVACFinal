#Brian West
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
import math
from collections import defaultdict
import csv
from sklearn.cluster import KMeans

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
fileColumnNames = defaultdict(list)
for filename in os.listdir(terminalFiles):
    fileData = pd.read_csv(os.path.join(terminalFiles,filename))
    for colName, colData in fileData.items():
        if setPoint in colName:
            fileData[colName] = fileData[colName].ffill()
        if colName in fileColumnNames:
            fileColumnNames[colName].append(filename)
        else:
            fileColumnNames[colName] = [filename]
    #per jeff's email
    fileData.drop(columns = ['Air_Flow_Diff'], inplace=True)
    fileData.drop(columns = ['Room_Temperature_Diff'], inplace=True)
    fileData.drop(columns = ['VAV_Temperature_Diff'], inplace=True)
    fileData.drop(columns = ['SaTemp'], inplace=True, errors='ignore') # SaTemp and SaTmp are the same column
    fileData.drop(columns = ['SaTmp'], inplace=True, errors='ignore')
    fileData.drop(columns = ['oppMode'], inplace=True)
    #remove columns with std of 0, anything with an errors = ignore are not in all files
    fileData.drop(columns = ['EffOcc'], inplace=True)
    fileData.drop(columns = ['Heating_Stg_Cmd'], inplace=True, errors='ignore')
    fileData.drop(columns = ['OccCmd'], inplace=True)
    fileData.drop(columns = ['SuplFanCmd'], inplace=True, errors='ignore')
    fileData.drop(columns = ['SuplFanState'], inplace=True, errors='ignore')
    fileData.drop(columns = ['Cooling_Stg_Cmd'], inplace=True, errors='ignore')
    fileData.drop(columns = ['AirflowSpRht'], inplace=True, errors='ignore')
    fileData.drop(columns = ['RmCo2'], inplace=True, errors='ignore')

    fileData.dropna(inplace=True)
    fileData.to_csv(os.path.join(cleanTerminalFiles,filename),index=False)


            
# #merge all the files into one file
terminalUnitsCleanData = pd.DataFrame()
for filename in os.listdir(cleanTerminalFiles):
    terminalDesignation = (os.path.splitext(filename)[0])
    fileData = pd.read_csv(os.path.join(cleanTerminalFiles,filename))
    
    fileData.insert(1,'designation',terminalDesignation)                     
    terminalUnitsCleanData = pd.concat([terminalUnitsCleanData,fileData])

terminalUnitsCleanData.to_csv('data/terminalUnitsCleanData.csv',index=False)

file = open('data/fileColumnNames.txt','w')
for key, value in fileColumnNames.items():
    file.write(key + '\n')
    files = ','.join(value)
    file.write(files)
    file.write('\n\n')
file.close()

#get basic stats on all columns
file = open("data/terminalDescription.txt", "w")
file.write("Total Rows\n")
file.write(str(len(terminalUnitsCleanData)))
file.write("\n\n")

for colName, data in terminalUnitsCleanData.items():
    file.write(colName)
    file.write("\n")
    file.write(data.describe().to_string())
    file.write("\n\n")
file.close()

#merge all the files into one file

rawRTU1 = pd.read_csv('data/roofTopUnits/RTU_1.csv')
rawRTU2 = pd.read_csv('data/roofTopUnits/RTU_2.csv')
rawRTU3 = pd.read_csv('data/roofTopUnits/RTU_3.csv') # different columns? different type of unit

rawRTU1.drop(columns=['oppMode'], inplace=True)
rawRTU2.drop(columns=['oppMode'], inplace=True)
rawRTU3.drop(columns=['oppMode'], inplace=True)

#cluster terminal units on time basis
# get distinct time stamps
timestamps = terminalUnitsCleanData['time'].unique()
designations = terminalUnitsCleanData['designation'].unique()
timestamps.sort()

numberOfClusters = 2 #number of RTUs
num_inits = 10
num_max_iter = 300
interias = []


km = KMeans(n_clusters = numberOfClusters, n_init = num_inits, max_iter = num_max_iter)

#create dataframe for that timestamp
clusterCount = {}
count = 0
for timestamp in timestamps:
    terminalData = terminalUnitsCleanData.loc[terminalUnitsCleanData['time'] == timestamp]
    if len(terminalData) == 47:
        count = count + 1 
        clusterData =  km.fit_predict(terminalData.drop(columns = ['time','designation']))
        terminalData.insert(0,'cluster', clusterData)
        cluster0 = terminalData[terminalData['cluster'] == 0]
        cluster1 = terminalData[terminalData['cluster'] == 1]
        cluster0String = ','.join(cluster0['designation'].tolist())
        cluster1String = ','.join(cluster1['designation'].tolist())
        if cluster0String in clusterCount:
            clusterCount[cluster0String] = clusterCount[cluster0String] + 1
        else:
            clusterCount[cluster0String] = 1
        if cluster1String in clusterCount:
            clusterCount[cluster1String] = clusterCount[cluster1String] + 1
        else:
            clusterCount[cluster1String] = 1

print(clusterCount)
print(count)

        
        

