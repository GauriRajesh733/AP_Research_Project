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
    
# total resting values
restingValues = []

# total stress values
stressValues = []

# rmssd
restingRMSSDValues = []
stressRMSSDValues = []

# pnn50
restingPNN50Values = []
stressPNN50Values = []

# sdnn
restingSDNNValues = []
stressSDNNValues = []

# mean_hr
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
                count = count + 1 
        for values in entry['stress']:
            stressValues.append(values)
            
print("resting values: ")
print("length: ")
print(len(restingValues))
print("mean: ")
print(np.mean(restingValues))
print("median: ")
print(np.median(restingValues))
print("range: ")
print(max(restingRMSSDValues)-min(restingRMSSDValues))

print("stress values: ")
print("length: ")
print(len(stressValues))
print("mean: ")
print(np.mean(stressValues))
print("median: ")
print(np.median(stressValues))

# Kolmorogov-Smirnov Test
resting_RMSSD_KS_Test = []
resting_RMSSD_KS_Test.extend(['resting RMSSD', kstest(restingRMSSDValues, 'norm').statistic, kstest(restingRMSSDValues, 'norm').pvalue]) 
stress_RMSSD_KS_Test = []
stress_RMSSD_KS_Test.extend(['stress RMSSD', kstest(stressRMSSDValues, 'norm').statistic, kstest(stressRMSSDValues, 'norm').pvalue])

resting_PNN50_KS_Test = []
resting_PNN50_KS_Test.extend(['resting PNN50', kstest(restingPNN50Values, 'norm').statistic, kstest(restingPNN50Values, 'norm').pvalue]) 
stress_PNN50_KS_Test = []
stress_PNN50_KS_Test.extend(['stress PNN50', kstest(stressPNN50Values, 'norm').statistic, kstest(stressPNN50Values, 'norm').pvalue])

resting_SDNN_KS_Test = []
resting_SDNN_KS_Test.extend(['resting SDNN', kstest(restingSDNNValues, 'norm').statistic, kstest(restingSDNNValues, 'norm').pvalue]) 
stress_SDNN_KS_Test = []
stress_SDNN_KS_Test.extend(['stress SDNN', kstest(stressSDNNValues, 'norm').statistic, kstest(stressSDNNValues, 'norm').pvalue])

resting_MeanHR_KS_Test = []
resting_MeanHR_KS_Test.extend(['resting MeanHR', kstest(restingMeanHRValues, 'norm').statistic, kstest(restingMeanHRValues, 'norm').pvalue]) 
stress_MeanHR_KS_Test = []
stress_MeanHR_KS_Test.extend(['stress MeanHR', kstest(stressMeanHRValues, 'norm').statistic, kstest(stressMeanHRValues, 'norm').pvalue]) 

KS_Test_Data = [resting_RMSSD_KS_Test, stress_RMSSD_KS_Test, resting_PNN50_KS_Test, stress_PNN50_KS_Test,resting_SDNN_KS_Test, stress_SDNN_KS_Test,resting_MeanHR_KS_Test, stress_MeanHR_KS_Test]
df = pd.DataFrame(KS_Test_Data, columns = ['HRV Parameter', 't statistic','p value'])
print(df)
df.to_csv(r'C:\Users\gauri\Desktop\AP Research Data\actual_experiments\resting_vs_stress_graphs\KS_TestResults.csv',index = False)

# Wilcoxon Signed Rank Test
RMSSD_W_Test = []
RMSSD_W_Test.extend(['RMSSD', wilcoxon(restingRMSSDValues, stressRMSSDValues).statistic, wilcoxon(restingRMSSDValues, stressRMSSDValues).pvalue])

SDNN_W_Test = []
SDNN_W_Test.extend(['SDNN', wilcoxon(restingSDNNValues, stressSDNNValues).statistic, wilcoxon(restingSDNNValues, stressSDNNValues).pvalue])

PNN50_W_Test = []
PNN50_W_Test.extend(['PNN50', wilcoxon(restingPNN50Values, stressPNN50Values).statistic, wilcoxon(restingPNN50Values, stressPNN50Values).pvalue])

MeanHR_W_Test = []
MeanHR_W_Test.extend(['MeanHR', wilcoxon(restingMeanHRValues, stressMeanHRValues).statistic, wilcoxon(restingMeanHRValues, stressMeanHRValues).pvalue])

W_Test_Data = [RMSSD_W_Test, PNN50_W_Test, SDNN_W_Test, MeanHR_W_Test]
df2 = pd.DataFrame(W_Test_Data, columns = ['HRV Parameter', 't statistic','p value'])
print(df2)
df2.to_csv(r'C:\Users\gauri\Desktop\AP Research Data\actual_experiments\resting_vs_stress_graphs\W_TestResults.csv',index = False)

# Boxplots

# RMSSD
plt.boxplot([restingRMSSDValues, stressRMSSDValues], patch_artist = True, boxprops = dict(facecolor = 'lightblue'))
plt.title('RMSSD (ms)')
plt.xticks([1,2],['Resting', 'Stress'])
plt.ylabel('Apple Watch Values')
plt.show()

# SDNN
plt.boxplot([restingSDNNValues, stressSDNNValues], patch_artist = True, boxprops = dict(facecolor = 'lightblue'))
plt.title('SDNN (ms)')
plt.xticks([1,2],['Resting', 'Stress'])
plt.ylabel('Apple Watch Values')
plt.show()

# pNN50
plt.boxplot([restingPNN50Values, stressPNN50Values], patch_artist = True, boxprops = dict(facecolor = 'lightblue'))
plt.title('pNN50 (%)')
plt.xticks([1,2],['Resting', 'Stress'])
plt.ylabel('Apple Watch Values')
plt.show()

# MeanHR
plt.boxplot([restingMeanHRValues, stressMeanHRValues], patch_artist = True, boxprops = dict(facecolor = 'lightblue'))
plt.title('HRM (bpm)')
plt.xticks([1,2],['Resting', 'Stress'])
plt.ylabel('Apple Watch Values')
plt.show()

# resting
restingRMSSDValues_median = np.median(restingRMSSDValues)
restingRMSSDValues_25 = np.percentile(restingRMSSDValues,25)
restingRMSSDValues_75 = np.percentile(restingRMSSDValues,75)
restingRMSSDValues_Range = np.ptp(restingRMSSDValues)
restingRMSSDValues_BP = []
restingRMSSDValues_BP.extend(['Resting RMSSD', restingRMSSDValues_25, restingRMSSDValues_median, restingRMSSDValues_75, restingRMSSDValues_Range])

restingSDNNValues_median = np.median(restingSDNNValues)
restingSDNNValues_25 = np.percentile(restingSDNNValues,25)
restingSDNNValues_75 = np.percentile(restingSDNNValues,75)
restingSDNNValues_Range = np.ptp(restingSDNNValues)
restingSDNNValues_BP = []
restingSDNNValues_BP.extend(['Resting SDNN', restingSDNNValues_25, restingSDNNValues_median, restingSDNNValues_75, restingSDNNValues_Range])

restingPNN50Values_median = np.median(restingPNN50Values)
restingPNN50Values_25 = np.percentile(restingPNN50Values,25)
restingPNN50Values_75 = np.percentile(restingPNN50Values,75)
restingPNN50Values_Range = np.ptp(restingPNN50Values)
restingPNN50Values_BP = []
restingPNN50Values_BP.extend(['Resting PNN50', restingPNN50Values_25, restingPNN50Values_median, restingPNN50Values_75, restingPNN50Values_Range])

restingMeanHRValues_median = np.median(restingMeanHRValues)
restingMeanHRValues_25 = np.percentile(restingMeanHRValues,25)
restingMeanHRValues_75 = np.percentile(restingMeanHRValues,75)
restingMeanHRValues_Range = np.ptp(restingMeanHRValues)
restingMeanHRValues_BP = []
restingMeanHRValues_BP.extend(['Resting MeanHR', restingMeanHRValues_25, restingMeanHRValues_median, restingMeanHRValues_75, restingMeanHRValues_Range])

# stress
stressRMSSDValues_median = np.median(stressRMSSDValues)
stressRMSSDValues_25 = np.percentile(stressRMSSDValues,25)
stressRMSSDValues_75 = np.percentile(stressRMSSDValues,75)
stressRMSSDValues_Range = np.ptp(stressRMSSDValues)
stressRMSSDValues_BP = []
stressRMSSDValues_BP.extend(['Stress RMSSD', stressRMSSDValues_25, stressRMSSDValues_median, stressRMSSDValues_75, stressRMSSDValues_Range])

stressSDNNValues_median = np.median(stressSDNNValues)
stressSDNNValues_25 = np.percentile(stressSDNNValues,25)
stressSDNNValues_75 = np.percentile(stressSDNNValues,75)
stressSDNNValues_Range = np.ptp(stressSDNNValues)
stressSDNNValues_BP = []
stressSDNNValues_BP.extend(['Stress SDNN', stressSDNNValues_25, stressSDNNValues_median, stressSDNNValues_75, stressSDNNValues_Range])

stressPNN50Values_median = np.median(stressPNN50Values)
stressPNN50Values_25 = np.percentile(stressPNN50Values,25)
stressPNN50Values_75 = np.percentile(stressPNN50Values,75)
stressPNN50Values_Range = np.ptp(stressPNN50Values)
stressPNN50Values_BP = []
stressPNN50Values_BP.extend(['Stress PNN50', stressPNN50Values_25, stressPNN50Values_median, stressPNN50Values_75, stressPNN50Values_Range])

stressMeanHRValues_median = np.median(stressMeanHRValues)
stressMeanHRValues_25 = np.percentile(stressMeanHRValues,25)
stressMeanHRValues_75 = np.percentile(stressMeanHRValues,75)
stressMeanHRValues_Range = np.ptp(stressMeanHRValues)
stressMeanHRValues_BP = []
stressMeanHRValues_BP.extend(['Stress MeanHR', stressMeanHRValues_25, stressMeanHRValues_median, stressMeanHRValues_75, stressMeanHRValues_Range])

BP_Test_Data = [restingRMSSDValues_BP, stressRMSSDValues_BP, restingSDNNValues_BP, stressSDNNValues_BP, restingPNN50Values_BP, stressPNN50Values_BP, restingMeanHRValues_BP, stressMeanHRValues_BP]
df3 = pd.DataFrame(BP_Test_Data, columns = ['HRV Parameter', 'Q1','Median','Q3', 'Range'])
print(df3)
df3.to_csv(r'C:\Users\gauri\Desktop\AP Research Data\actual_experiments\resting_vs_stress_graphs\BP_Results.csv',index = False)