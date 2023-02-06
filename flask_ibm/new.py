import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "8Q9n8K8Wq9Asg1QjULQwdj8K8liF4hy2aQD1cOi1lyDc"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field":[['City', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3','Benzene', 'Toluene', 'Xylene', 'Year', 'Month']] , 
                                   "values": [[18,3,2,2,1,2,1,5,4,2,3,2,1,2022,6]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/23566e07-99c4-4fd0-a52e-7953832ca7d1/predictions?version=2022-07-19', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
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
print(res)