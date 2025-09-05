# Stress Detection with Smartwatches

[**Final Paper**](https://drive.google.com/file/d/1dc5VqZodXUlEKjaarF4qZAdfQVxDm_KZ/view)

In my senior year of high school, I was able to take AP Research and conduct a yearlong study on a topic of my choice.  My preliminary research on the growing wearable technology market and its increasing applications to healthcare led me to focus on how smartwatch heart rate variability data can be used to detect stress in high school students.  

Through this project, I developed Python code to extract, preprocess, store, and analyze participant HRV data using open source modules including hrv-analysis, Pandas, Matplotlib, Numpy, SciPy, and scikit-learn.  I also created a logistic regression (LR) model to assess how effectively Apple Watch HRV measurements could be used to detect stressed and resting states in participants

---

## Why I Built This

Through this project, I wanted to build upon my programming skills, understand how to work with real world data, and explore basic machine learning concepts.  My interest in research at the interesection of biology, psychology, and computer science also shaped my research inquiry.

---

## Features

### Preprocess and Organize HRV Data

- After collecting participant HR data using the Apple Watch Breathe app during experiments, data is exported from the Apple Health Records app in XML format
- [**preprocess.py**](preprocessing.py) extracts HR data from the Apple Health Records XML file and creates 2 csv files for a given participant containing resting and stressed raw RR interval values.  
- The raw RR intervals during resting and stressed stages of the experiment are displayed in two graphs.  
- The raw RR intervals are preprocessed and HRV parameters are calculated.  
- This data from each participant is then stored in JSON format.      

### Statistical Analysis

- Using the JSON file with all participant data, [**statistics.py**](statistics.py) performs the Kolmorogov-Smirnov and Wilcoxon Signed Rank tests on the calculated HRV parameters (rmssd, sdnn, pnn50, meanHR).
- Boxplots comparing resting and stressed values for all HRV parameters are also created.

### Linear Regression Model

- [**logistic_regression_load_data.py**](logistic_regression_load_data.py) uses the JSON file with all participant data to create a single csv file with rmssd, sdnn, pnn50, and hrm values.
- An additional column called "Label" indicates whether the HRV parameters in a given row were measured during resting or stressed stages of the experiment.
- The label 0 is associated with resting whereas the label 1 is associated with stress.
- After all the data has been added to a single csv file, [**logistic_regression.py**](logistic_regression.py) creates a logistic regression machine learning model.
- The purpose of [**logistic_regression.py**](logistic_regression.py) was to determine to what extent smartwatch HRV measurements can be used to differentiate between resting and stressed states in participants.

---

## What I Learned

Through the research process, I learned to conduct a literature review to inform my own study, break down complex programs into manageable components, and efficiently manage my time to fit participant experiments into my schedule as well as make work on my final paper.

Seeing how programming can be used to analyze real world data, this project has contributed to my interest in the applications of computer science to challenges in healthcare.  
