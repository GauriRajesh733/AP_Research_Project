# import pandas
import pandas as pd

# load dataset containing HRV features for all participants including 0 or 1 label
# 0 represents resting state whereas 1 represents stressed state values
df = pd.read_csv(r"C:\Users\gauri\Desktop\AP Research Data\actual_experiments\regressiontesting\HRVFeaturesOLDCSV.csv")

print(df.head())

# split dataset into features and target variable
feature_cols = ['RMSSD', 'SDNN', 'pNN50', 'HRM']

X = df[feature_cols]
y = df.Label

# split X and y into training and testing sets
from sklearn.model_selection import train_test_split

# 25% of dataset used for testing
# returns 4 arrays that can be used to train and test ML model
# random state sets seed number
X_train, X_test, y_train, y_test = train_test_split (X, y, test_size = 0.2, random_state = 16, stratify=y)
print(y_train)
print(y_test)

'''
#standardize features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
'''
'''
#normalize features
#more appropriate because distribution is not assumed to be normal
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
'''

# import logisticregression class
from sklearn.linear_model import LogisticRegression

# create model object
logreg = LogisticRegression(max_iter = 1000, random_state = 16)

# fit or train model with data
logreg.fit(X_train, y_train)

# store predictions in y_pred
y_pred = logreg.predict(X_test)

# evaluate model with confusion matrix

# import metric class
from sklearn import metrics

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

# visualize confusion matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class_names = ['0','1']
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.show()

# evaluate model using classification_report for accuracy, precision, and recall
from sklearn.metrics import classification_report
target_names = ['relax', 'stress']
print(classification_report(y_test, y_pred, target_names = target_names))

# ROC curve to plot true positive rate against false positive rate
# show tradeoff between sensitivity and specificity
# AUC score of 1 is perfect classifier, while 0.5 is worthless classifier
y_pred_proba = logreg.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()
