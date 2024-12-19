#import modules
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json
from scipy.stats import kstest
from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu
import pandas as pd


with open(r"C:\Users\gauri\Desktop\AP Research Data\programs\json\testWORKINGJSON.json", 'r') as openfile:
    myRootJson = json.load(openfile)
    
#total resting values
restingValues = []

#total stress values
stressValues = []

#rmssd
restingRMSSDValues = []
stressRMSSDValues = []

#pnn50
restingPNN50Values = []
stressPNN50Values = []

#sdnn
restingSDNNValues = []
stressSDNNValues = []

#mean_hr
restingMeanHRValues = []
stressMeanHRValues = []

participants = {}
participants = myRootJson['participants']
count = 0

for student in participants:
    for entry in student['hrv features']:
        restingRMSSDValues.append(entry['resting']['rmssd'])
        stressRMSSDValues.append(entry['stress']['rmssd'])
        
        restingPNN50Values.append(entry['resting']['pnni_50'])
        stressPNN50Values.append(entry['stress']['pnni_50'])

        restingSDNNValues.append(entry['resting']['sdnn'])
        stressSDNNValues.append(entry['stress']['sdnn'])

        restingMeanHRValues.append(entry['resting']['mean_hr'])
        stressMeanHRValues.append(entry['stress']['mean_hr'])
for student in participants:
    for entry in student['processed RR intervals']:
        for values in entry['resting']:
            if (count < 18338):
                restingValues.append(values)
                count = count + 1 #randomize this process?
        for values in entry['stress']:
            stressValues.append(values)


#create csv file
            
fname = r"C:\Users\gauri\Desktop\AP Research Data\actual_experiments\regressiontesting\HRVFeaturesOLDCSV.csv"
mycsv = open(fname, 'w')
line = 'RMSSD,SDNN,pNN50,HRM,Label' + '\n'
mycsv.write(line)
print(len(restingRMSSDValues))
#add to csv file
for i in range(len(restingRMSSDValues)):
    #add resting values
    restingRMSSD = restingRMSSDValues[i]
    restingSDNN = restingSDNNValues[i]
    restingPNN50 = restingPNN50Values[i]
    restingMeanHR = restingMeanHRValues[i]
    line = str(restingRMSSD) + ',' + str(restingSDNN) + ','+ str(restingPNN50) + ',' + str(restingMeanHR) + ',' + '0' + '\n'
    mycsv.write(line)
    #add stress values
    stressRMSSD = stressRMSSDValues[i]
    stressSDNN = stressSDNNValues[i]
    stressPNN50 = stressPNN50Values[i]
    stressMeanHR = stressMeanHRValues[i]
    line = str(stressRMSSD) + ',' + str(stressSDNN) + ','+ str(stressPNN50) + ',' + str(stressMeanHR) + ',' + '1' + '\n'
    mycsv.write(line)


mycsv.close()


restingRMSSD = []
restingSDNN = []
restingPNN50 = []
restingMeanHR = []
restingLabels = []
stressRMSSD = []
stressSDNN = []
stressPNN50 = []
stressMeanHR = []
stressLabels = []

for i in range(len(restingRMSSDValues)):
    #add resting values
    restingRMSSD.append(restingRMSSDValues[i])
    restingSDNN.append(restingSDNNValues[i])
    restingPNN50.append(restingPNN50Values[i])
    restingMeanHR.append(restingMeanHRValues[i])
    restingLabels.append(0)
    #add stress values
    stressRMSSD.append(stressRMSSDValues[i])
    stressSDNN.append(stressSDNNValues[i])
    stressPNN50.append(stressPNN50Values[i])
    stressMeanHR.append(stressMeanHRValues[i])
    stressLabels.append(1)

dict = {'RMSSD': restingRMSSD + stressRMSSD, 'SDNN': restingSDNN + stressSDNN, 'pNN50': restingPNN50+ stressPNN50, 'HRM': restingMeanHR + stressMeanHR, 'Label': restingLabels + stressLabels}

df = pd.DataFrame(dict)
print(df)
df.to_csv(r"C:\Users\gauri\Desktop\AP Research Data\actual_experiments\regressiontesting\HRVFeaturesCORRECTCSV.csv", index = False)
    




