import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

import warnings
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)

import model
import app

df = model.get_dataframe_from_obj_storage("cc-tutorial3600", app.csvName)
		
dataset = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

# Import label encoder 
from sklearn import preprocessing 
   
# label_encoder object knows how to understand word labels. 
label_encoder = preprocessing.LabelEncoder() 
  
# Encode labels in column 'Geography'. 
dataset['Geography']= label_encoder.fit_transform(dataset['Geography']) 
  
dataset['Geography'].unique() 

#france - 0
#germany - 1
#spain - 2

# Encode labels in column 'Gender'. 
dataset['Gender']= label_encoder.fit_transform(dataset['Gender']) 
  
dataset['Gender'].unique() 

#male - 1
#female - 0

X =  dataset.drop(['Exited'], axis=1)
y = dataset['Exited']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=200, random_state=0)  
classifier.fit(X_train, y_train)  
predictions = classifier.predict(X_test)

#code to create and save the plot locally

#report

feat_importances = pd.Series(classifier.feature_importances_, index=X.columns)
fig, ax = plt.subplots()
feat_importances.nlargest(10).plot(kind='barh')
fig.set_size_inches(18.5, 10.5, forward=True)
fig.savefig('./static/report_one.png', dpi=100)

#is active member

fig, ax = plt.subplots()
exited = dataset[dataset['Exited']==1]['IsActiveMember'].value_counts()
retained = dataset[dataset['Exited']==0]['IsActiveMember'].value_counts()
df = pd.DataFrame([exited, retained])
df.index = ['Left','Stayed']
df.plot(kind='bar',stacked=True, figsize=(10,5), ax=ax)
ax.legend(["not an active member", "active member"])
for tick in ax.get_xticklabels():
    tick.set_rotation(360)
fig.set_size_inches(18.5, 10.5, forward=True)
fig.savefig('./static/report_three.png', dpi=100)
#gender

fig, ax = plt.subplots()
exited = dataset[dataset['Exited']==1]['Gender'].value_counts()
retained = dataset[dataset['Exited']==0]['Gender'].value_counts()
df = pd.DataFrame([exited, retained])
df.index = ['Left','Stayed']
df.plot(kind='bar',stacked=True, figsize=(10,5), ax=ax)


fig, ax = plt.subplots()
exited = dataset[dataset['Exited']==1]['HasCrCard'].value_counts()
retained = dataset[dataset['Exited']==0]['HasCrCard'].value_counts()
df = pd.DataFrame([exited, retained])
df.index = ['Left','Stayed']
df.plot(kind='bar',stacked=True, figsize=(10,5), ax=ax)
ax.legend(["doesn't have credit card", "has credit card"])
for tick in ax.get_xticklabels():
    tick.set_rotation(360)
fig.set_size_inches(18.5, 10.5, forward=True)
fig.savefig('./static/report_five.png', dpi=100)

#geography

fig, ax = plt.subplots()
exited = dataset[dataset['Exited']==1]['Geography'].value_counts()
retained = dataset[dataset['Exited']==0]['Geography'].value_counts()
df = pd.DataFrame([exited, retained])
df.index = ['Left','Stayed']
df.plot(kind='bar',stacked=True, figsize=(10,5), ax=ax)
ax.legend(["france", "germany", "spain"])
for tick in ax.get_xticklabels():
    tick.set_rotation(360)
fig.set_size_inches(18.5, 10.5, forward=True)
fig.savefig('./static/report_six.png', dpi=100)