from flask import Flask, render_template, request
import pickle, joblib
import pandas as pd

app = Flask(__name__)

le = joblib.load('label_values')

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "8Q9n8K8Wq9Asg1QjULQwdj8K8liF4hy2aQD1cOi1lyDc"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/index.html')
def predict():
    return render_template("index.html")

@app.route('/output.html', methods =["POST","GET"])
def output():
    if request.method == 'POST': 
        city = request.form["city"]
        pm25 = request.form["pm25"]
        pm10 = request.form["pm10"]
        no = request.form["no"]
        no2 = request.form["no2"]
        nox = request.form["nox"]
        nh3 = request.form["nh3"]
        co = request.form["co"]
        so2 = request.form["so2"]
        o3 = request.form["o3"]
        benzene = request.form["benzene"]
        toluene = request.form["toluene"]
        xylene = request.form["xylene"]
        date = request.form["date"]
    
        city = le.transform([city])
        city=str(city[0])
        
        year = date.split('-')[0]
        month = date.split('-')[1]
        
        feature_cols = ['City', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 
                        'O3','Benzene', 'Toluene', 'Xylene', 'Year', 'Month']
        vals = [city,pm25,pm10,no,no2,nox,nh3,co,so2,o3,
                              benzene,toluene,xylene,year,month]
        print(vals)
        
        
        payload_scoring = {"input_data": [{"field":[feature_cols] , 
                                           "values": [vals]}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/23566e07-99c4-4fd0-a52e-7953832ca7d1/predictions?version=2022-07-19', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        #print("Scoring response")
        preds = response_scoring.json()
        pred = preds['predictions'][0]['values'][0][0]
        if (pred>=0 and pred<=50):
            res = 'GOOD'
        elif (pred>50 and pred<=100):
            res= 'SATISFACTORY'
        elif (pred>100 and pred<=200):
            res = 'MODERATELY POLLUTED'
        elif (pred>200 and pred<=300):
            res = 'POOR'
        elif (pred>300 and pred<=400):
            res = 'VERY POOR'
        else:
            res = 'SEVERE'
        #print(res)
        
    
        
        return render_template("output.html",y=("AQI: "+str(pred)), z =res)

if __name__ == '__main__':
    app.run(debug = False)