from flask import Flask, render_template, request
import pickle, joblib
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))
le = joblib.load('label_values')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/index.html')
def predict():
    return render_template("index.html")

@app.route('/output.html', methods =["POST"])
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
        
        year = date.split('-')[0]
        month = date.split('-')[1]
        
        feature_cols = ['City', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 
                        'O3','Benzene', 'Toluene', 'Xylene', 'Year', 'Month']
        
        data = pd.DataFrame([[city,pm25,pm10,no,no2,nox,nh3,co,so2,o3,
                              benzene,toluene,xylene,year,month]], columns=feature_cols)
        
        pred = model.predict(data)
        pred=pred[0]
        
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
        
        return render_template("output.html",y=("AQI: "+str(pred)), z =res)

if __name__ == '__main__':
    app.run(debug = True)