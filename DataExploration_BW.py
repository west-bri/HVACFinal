# Authors : Brian West, Bini Chandra, Cody Snow

# Importing required libraries
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

# Path setup
currentFolder = os.getcwd()
print(currentFolder)
terminalFiles = currentFolder + '/data/terminalUnits'
roofTopFiles = currentFolder + '/data/roofTopUnits'
cleanTerminalFiles = currentFolder +'/data/cleanTerminalUnits'

rawRTU1 = pd.read_csv('data/roofTopUnits/RTU_1.csv')
rawRTU2 = pd.read_csv('data/roofTopUnits/RTU_2.csv')
rawRTU3 = pd.read_csv('data/roofTopUnits/RTU_3.csv') # different columns? different type of unit

setPoint = 'Sp'



# rawRTU1 = pd.read_csv('data/roofTopUnits/RTU_1.csv')
# rawRTU2 = pd.read_csv('data/roofTopUnits/RTU_2.csv')
# rawRTU3 = pd.read_csv('data/roofTopUnits/RTU_3.csv') # different columns? different type of unit


# Cleaning TU files (forward-fill setpoints + drop unwanted columns)

fileColumnNames = defaultdict(list)
for filename in os.listdir(terminalFiles):
    fileData = pd.read_csv(os.path.join(terminalFiles,filename))

    # Forward-fill all setpoint-related columns
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



    #  Dropping unnecessary columns(as per client's suggestion)      
    fileData.drop(columns = ['Air_Flow_Diff', 'Room_Temperature_Diff', 'VAV_Temperature_Diff', 'SaTemp', 'oppMode'], inplace=True, errors='ignore')
    fileData.to_csv(os.path.join(cleanTerminalFiles,filename))    


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

file = open("data/RTUdescription.txt", "w")
file.write("Total Rows RTU1\n")
file.write(str(len(rawRTU1)))
file.write("\n\n")
for colName, data in rawRTU1.items():
    file.write(colName)
    file.write("\n")
    file.write(data.describe().to_string())
    file.write("\n\n")
file.write("Total Rows RTU2\n")
file.write(str(len(rawRTU2)))
file.write("\n\n")
for colName, data in rawRTU2.items():
    file.write(colName)
    file.write("\n")
    file.write(data.describe().to_string())
    file.write("\n\n")
file.write("Total Rows RTU3\n")
file.write(str(len(rawRTU3)))
file.write("\n\n")
for colName, data in rawRTU3.items():
    file.write(colName)
    file.write("\n")
    file.write(data.describe().to_string())
    file.write("\n\n")
file.close()

#merge all the files into one file

rawRTU1 = pd.read_csv('data/roofTopUnits/RTU_1.csv')
rawRTU2 = pd.read_csv('data/roofTopUnits/RTU_2.csv')
rawRTU3 = pd.read_csv('data/roofTopUnits/RTU_3.csv') # different columns? different type of unit

timelessRTU1 = rawRTU1
timelessRTU1.drop(columns=['time'], inplace=True)
timelessRTU2 = rawRTU2
timelessRTU2.drop(columns=['time'], inplace=True)
timelessRTU3 = rawRTU3
timelessRTU3.drop(columns=['time'], inplace=True)

print()

# Initialise list to collect mean correlation values
heatmap_data = []

#approach find correlation between ALL RTU columns and ALL terminal unit columns (except time lol)
sorted_tu_files = sorted(os.listdir(cleanTerminalFiles))
for filename in sorted_tu_files:
    fileData = pd.read_csv(os.path.join(cleanTerminalFiles,filename))
    fileData.drop(columns=['time'], inplace=True)
    corr1 = timelessRTU1.corrwith(fileData)
    corr2 = timelessRTU2.corrwith(fileData)
    corr3 = timelessRTU3.corrwith(fileData)
    corr1.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU1.csv')
    corr2.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU2.csv')
    corr3.to_csv(f'data/correlation/{os.path.splitext(filename)[0]}_RTU3.csv')

    # Calculate mean correlation for each RTU
    corrMean1 = corr1.mean(skipna=True)
    corrMean2 = corr2.mean(skipna=True)
    corrMean3 = corr3.mean(skipna=True)
    
    heatmap_data.append([corrMean1, corrMean2, corrMean3])

heatmap_df = pd.DataFrame(heatmap_data, 
                          columns=['RTU 1', 'RTU 2', 'RTU 3'], 
                          index=[os.path.splitext(f)[0] for f in sorted_tu_files])

# Create and save heatmap
plt.figure(figsize=(12, 16))
sns.heatmap(heatmap_df, annot=True, cmap='YlGnBu', linewidths=0.5)
plt.title('Average Correlation between each TU and RTUs')
plt.xlabel('RTUs')
plt.ylabel('Terminal Units')
plt.tight_layout()
plt.savefig("data/TU_RTU_Correlation_Heatmap.png")
plt.show()




#PCA requires data to be filled in
#clustering is worthless without having some summarized metric for each terminal unit. Maybe averaging values?
rawRTU1.drop(columns=['oppMode'], inplace=True)
rawRTU2.drop(columns=['oppMode'], inplace=True)
rawRTU3.drop(columns=['oppMode'], inplace=True)



#Clustering Terminal Units was not successful. only 65% accuracy. 
#cluster terminal units on time basis
# get distinct time stamps
# timestamps = terminalUnitsCleanData['time'].unique()
# designations = terminalUnitsCleanData['designation'].unique()
# timestamps.sort()

# numberOfClusters = 2 #number of RTUs
# num_inits = 10
# num_max_iter = 300
# interias = []


# km = KMeans(n_clusters = numberOfClusters, n_init = num_inits, max_iter = num_max_iter)

# #create dataframe for that timestamp
# clusterCount = {}
# count = 0
# for timestamp in timestamps:
#     terminalData = terminalUnitsCleanData.loc[terminalUnitsCleanData['time'] == timestamp]
#     if len(terminalData) == 47:
#         count = count + 1 
#         clusterData =  km.fit_predict(terminalData.drop(columns = ['time','designation']))
#         terminalData.insert(0,'cluster', clusterData)
#         cluster0 = terminalData[terminalData['cluster'] == 0]
#         cluster1 = terminalData[terminalData['cluster'] == 1]
#         cluster0String = ','.join(cluster0['designation'].tolist())
#         cluster1String = ','.join(cluster1['designation'].tolist())
#         if cluster0String in clusterCount:
#             clusterCount[cluster0String] = clusterCount[cluster0String] + 1
#         else:
#             clusterCount[cluster0String] = 1
#         if cluster1String in clusterCount:
#             clusterCount[cluster1String] = clusterCount[cluster1String] + 1
#         else:
#             clusterCount[cluster1String] = 1

# print(clusterCount)
# print(count)

        
        

