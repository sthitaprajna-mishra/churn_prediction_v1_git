import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, url_for, redirect


from model import classifier as loaded_model

import os

port = int(os.getenv("VCAP_APP_PORT"))

from model import credentials, re_values, re_labels, firstChartOne, firstChartTwo, secChartOne, secChartTwo, exitedAgeValues, exitedAgeLabels


app = Flask(__name__)

flask = 0

newUrl = ""
csvName = ""


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)


@app.route('/index')
def index():
    if flag == 0:
        return render_template('index.html', flag = 0)
    else:
        return render_template('index.html', flag = 1)

@app.route('/result', methods = ['POST']) 
def result(): 
    if request.method == 'POST': 
        to_predict_list = request.form.to_dict() 
        to_predict_list = list(to_predict_list.values()) 
        to_predict_list = list(map(float, to_predict_list)) 
        to_predict = np.array(to_predict_list).reshape(1, 10) 

        if(flag == 0):
            result = loaded_model.predict(to_predict)
        else:
            from new_model import classifier as new_loaded_model
            result = new_loaded_model.predict(to_predict)
        final_result = result[0]  

        if int(final_result)== 1: 
            prediction ='Customer will exit'
        else: 
            prediction ='Customer will not exit'  

        return render_template("result.html", prediction = prediction, values= re_values, 
        labels= re_labels, firstChartOne = firstChartOne, firstChartTwo = firstChartTwo,
        secChartOne = secChartOne, secChartTwo = secChartTwo, 
        exitedAgeValues = exitedAgeValues, exitedAgeLabels = exitedAgeLabels
        ) 




app.secret_key = "secret key"

import ibm_boto3

from ibm_botocore.client import Config
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

bucket_name = "cc-turoial3600"

resource = ibm_boto3.resource('s3',
                      ibm_api_key_id=credentials['apikey'],
                      ibm_service_instance_id=credentials['resource_instance_id'],
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

import urllib.request


@app.route('/upload')
def upload():
    return render_template('upload.html')
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        global flag
        flag = 1
        global newUrl
        newUrl = request.form['newUrl']
        global csvName
        csvName = request.form['csvName']
        resource.Bucket(name=bucket_name).put_object(Key=csvName, Body=urllib.request.urlopen(newUrl).read())


        
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = port)