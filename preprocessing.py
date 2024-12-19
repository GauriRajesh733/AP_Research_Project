from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values, get_time_domain_features
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as et
from datetime import datetime
import sys
import json

# DATA EXTRACTION

# Step 1: Get Apple Health export XML file
#apple_health_export = r""
tree = et.ElementTree(file = apple_health_export)
root = tree.getroot()

# Step 2: Create separate csv files for stressed and resting stages of experiment

# each participant is assigned a unique identification number
#id =

# add resting and stressed csv files of participants to separate folders for later analysis

# resting csv file
# TO DO: Dec 2024: process filename from command line args
#resting_fname = r""
resting_fname = resting_fname + "\Participant"+str(id)+"_Resting" + ".csv"
mycsv = open(resting_fname,"w")
line = "Start Date, End Date, BPM, Time, RR Interval (ms), RR Interval (s)" + "\n"
mycsv.write(line)

# stressed csv file
#stressed_fname = r""
stressed_fname = stressed_fname + "\Participant"+str(id)+"_Stress" + ".csv"
mycsv2 = open(stressed_fname,"w")
line2 = "Start Date, End Date, BPM, Time, RR Interval (ms), RR Interval (s)" + "\n"
mycsv2.write(line)

# parse Apple Health XML file
# TO DO: Dec 2024: process start and end dates of stress and resting tasks from command line args

# RESTING INTERVALS
for element in root.findall('Record'):
        if ("type" in element.attrib) and (element.attrib["type"] == "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"):
            if (("2024-03-05 15:11") in element.attrib['endDate'] or \
                ("2024-03-05 15:16") in element.attrib['endDate'] or \
                ("2024-03-12 14:34") in element.attrib['endDate'] or \
                ("2024-03-12 14:38") in element.attrib['endDate']):
                startDate = element.attrib['startDate']
                cleanedStartDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S %z").strftime("%B %d %Y %H:%M")
                endDate = element.attrib['endDate']
                cleanedEndDate = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S %z").strftime("%B %d %Y %H:%M")
                for metaDataListElement in element.findall('HeartRateVariabilityMetadataList'):
                    for bpmElement in metaDataListElement.findall('InstantaneousBeatsPerMinute'):
                        bpm = bpmElement.attrib['bpm']
                        timestamp = bpmElement.attrib['time']
                        cleanedTime = timestamp.encode("ascii", "ignore").decode("utf-8")
                        rrIntervalMS = str(60000/int(bpm))
                        rrIntervalS = str(60/int(bpm))
                        line = cleanedStartDate + "," + cleanedEndDate + "," + bpm + "," + cleanedTime + "," + rrIntervalMS + "," + rrIntervalS + "\n"
                        mycsv.write(line)

# STRESS INTERVALS                 
for element in root.findall('Record'):
        if ("type" in element.attrib) and (element.attrib["type"] == "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"):
            if (("2024-03-12 14:15") in element.attrib['endDate'] or \
                ("2024-03-12 14:23") in element.attrib['endDate'] or \
                ("2024-03-05 15:22") in element.attrib['endDate'] or \
                ("2024-03-05 15:28") in element.attrib['endDate']):
                startDate = element.attrib['startDate']
                cleanedStartDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S %z").strftime("%B %d %Y %H:%M")
                endDate = element.attrib['endDate']
                print(endDate)
                cleanedEndDate = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S %z").strftime("%B %d %Y %H:%M")
                for metaDataListElement in element.findall('HeartRateVariabilityMetadataList'):
                    for bpmElement in metaDataListElement.findall('InstantaneousBeatsPerMinute'):
                        bpm = bpmElement.attrib['bpm']
                        timestamp = bpmElement.attrib['time']
                        cleanedTime = timestamp.encode("ascii", "ignore").decode("utf-8")
                        rrIntervalMS = str(60000/int(bpm))
                        rrIntervalS = str(60/int(bpm))
                        line = cleanedStartDate + "," + cleanedEndDate + "," + bpm + "," + cleanedTime + "," + rrIntervalMS + "," + rrIntervalS + "\n"
                        mycsv2.write(line)
                  
mycsv.close()
mycsv2.close()

# Step 3: Graph Raw Data
df1 = pd.read_csv(resting_fname)
df2 = pd.read_csv(stressed_fname)
#print(df1.head())
#print(df2.head())

# DATA PREPROCESSING

# RESTING FILE
rr_intervals_list1 = df1[" RR Interval (ms)"].tolist()
rr_intervals_without_outliers1 = remove_outliers(rr_intervals = rr_intervals_list1, low_rri = 300, high_rri = 2000)
interpolated_rr_intervals1 = interpolate_nan_values(rr_intervals = rr_intervals_without_outliers1, interpolation_method = "linear")
nn_intervals_list1 = remove_ectopic_beats(rr_intervals = interpolated_rr_intervals1, method = "malik")
interpolated_nn_intervals1 = interpolate_nan_values(rr_intervals = nn_intervals_list1)

time_domain_features1 = get_time_domain_features(interpolated_nn_intervals1)

# STRESS FILE
rr_intervals_list2 = df2[" RR Interval (ms)"].tolist()
rr_intervals_without_outliers2 = remove_outliers(rr_intervals = rr_intervals_list2, low_rri = 300, high_rri = 2000)
interpolated_rr_intervals2 = interpolate_nan_values(rr_intervals = rr_intervals_without_outliers2, interpolation_method = "linear")
nn_intervals_list2 = remove_ectopic_beats(rr_intervals = interpolated_rr_intervals2, method = "malik")
interpolated_nn_intervals2 = interpolate_nan_values(rr_intervals = nn_intervals_list2)

time_domain_features2 = get_time_domain_features(interpolated_nn_intervals2)

# display graphs after preprocessing
plt.plot(df1.iloc[:,4], label='resting')
plt.plot(df2.iloc[:,4], label='stress')

plt.ylabel('RR Interval (ms)')
plt.xlabel('Time')
plt.title('Resting Vs Stress RR Intervals')
plt.xticks([])
plt.legend()
plt.show()

plt.plot(df1.iloc[:,4], label='resting raw')
plt.plot(interpolated_nn_intervals1, label='resting processed')

plt.ylabel('RR Interval (ms)')
plt.xlabel('Time')
plt.title('Resting Intervals')
plt.xticks([])
plt.legend()
plt.show()

# DATA STORAGE

# Step 4: Add participant data to JSON file
# include id #, processed RR intervals, HRV features
# (sdnn, pnni50, rmssd, mean_hr) for rest and stress periods

# open JSON file
with open(r"C:\Users\gauri\Desktop\AP Research Data\programs\json\testWORKINGJSON.json", 'r') as openfile:
    myRootJson = json.load(openfile)

# comment code below once json file created
'''
#myRootJson = {}
#myRootJson['participants'] = []
'''

# use code below to delete any duplicate participants made by accident
'''
myArray = myRootJson['participants']
myNewArray = []

for entry in myArray:
    if (entry['id #'] != 17):
        myNewArray.append(entry)

myRootJson['participants'] = myNewArray
'''

# first gen
myJson1 = {}
myJson1['id #'] = id
myJson1['processed RR intervals'] = []
myJson1['hrv features'] = []

# second gen: processed RR intervals
myJson2 = {}
myJson2['resting'] = interpolated_nn_intervals1
myJson2['stress'] = interpolated_nn_intervals2

# second gen: hrv features
myJson3 = {}
myJson3['resting'] = {}
for key,value in time_domain_features1.items():
    if (key == 'sdnn' or key == 'pnni_50' or key == 'rmssd' or key == 'mean_hr'):
        myJson3['resting'][key] = value

myJson3['stress'] = {}
for key,value in time_domain_features2.items():
    if (key == 'sdnn' or key == 'pnni_50' or key == 'rmssd' or key == 'mean_hr'):
        myJson3['stress'][key] = value

# add json objects to root json
myRootJson['participants'].append(myJson1)
myJson1['processed RR intervals'].append(myJson2)
myJson1['hrv features'].append(myJson3)

'''
#serializing json
json_object = json.dumps(myRootJson, indent = 2)

with open(r'C:/Users/gauri/Desktop/AP Research Data/programs/json/testWORKINGJSON.json', "w") as outfile:
    outfile.write(json_object)
'''