import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# import pickle
# import sqlite3

# conn = sqlite3.connect(r"C:\sqlite3\dbOne.db")
# customer_data = pd.read_sql_query("SELECT * from tableOne", conn)

bucket_name = 'cc-tutorial3600'

credentials = {
  #"insert your own crdentials"
}

import ibm_boto3

from ibm_botocore.client import Config
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.jp-tok.cloud-object-storage.appdomain.cloud'


resource = ibm_boto3.resource('s3',
                      ibm_api_key_id=credentials['apikey'],
                      ibm_service_instance_id=credentials['resource_instance_id'],
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)


import io

def get_dataframe_from_obj_storage(bucket_name, key):
    obj = resource.Object(bucket_name=bucket_name, key=key).get()
    return pd.read_csv(io.BytesIO(obj['Body'].read()))

df = get_dataframe_from_obj_storage("cc-tutorial3600", 'Churn_Modelling.csv')


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

#report

re_values = classifier.feature_importances_.tolist()
re_labels = X.columns.tolist()

#is active member

exited = dataset[dataset['Exited']==1]['IsActiveMember'].value_counts()
retained = dataset[dataset['Exited']==0]['IsActiveMember'].value_counts()

firstChartOne = exited.tolist()
firstChartTwo = retained.tolist()

#gender

exitedTwo = dataset[dataset['Exited']==1]['Gender'].value_counts()
retainedTwo = dataset[dataset['Exited']==0]['Gender'].value_counts()

secChartOne = exitedTwo.tolist()
secChartTwo = retainedTwo.tolist()


#credit card

exitedThree = dataset[dataset['Exited']==1]['HasCrCard'].value_counts()
retainedThree = dataset[dataset['Exited']==0]['HasCrCard'].value_counts()

thirdChartOne = exitedThree.tolist()
thirdChartTwo = retainedThree.tolist()


#age 

exitedAgeValues = dataset[dataset['Exited']==1]['Age'].value_counts().tolist()
exitedAgeLabels = dataset[dataset['Exited']==1]['Age'].unique().tolist()

