from flask import Flask, request, Response
import data.naivesBayes as NB
import data.dataSource as DS

app = Flask(__name__)

@app.route('/test')
def hello() :
    return {'msg':"Hello"}, 200

@app.route('/chart-data')
def get_barchart():
    data = DS.get_demographic_rates()
    return data, 200
    

@app.route('/demographics', methods=['POST'])
def get_demographics():
    age_options = ['0-17 years', '18-49 years', '50-64 years', '65+ years']
    sex = request.json['sex']
    age = request.json['age']
    comorbidity = request.json['comorbidity']
    symptomatic = request.json['symptomatic']
    curStat = request.json['currentStatus']

    if sex == '':
        return {'error': 'Sex Empty'}, 401
    if age == '':
        return {'error': 'Age Empty'}, 401
    if comorbidity == '':
        return {'error': 'Underlying Conditions Empty'}, 401
    if symptomatic == '':
        return {'error': 'Symptomatic Empty'}, 401
    if curStat == '':
        return {'error': 'COVID Status Empty'}, 401

    pred_arr = []
    for range in age_options:
        if age == range:
            pred_arr.append(1)
        else: 
            pred_arr.append(0)
    
    if sex == 'Female':
        pred_arr.append(1)
        pred_arr.append(0)
    else: 
        pred_arr.append(0)
        pred_arr.append(1)

    if comorbidity == 'No':
        pred_arr.append(1)
        pred_arr.append(0)
    else: 
        pred_arr.append(0)
        pred_arr.append(1)

    if symptomatic == 'Asymptomatic':
        pred_arr.append(1)
        pred_arr.append(0)
    else: 
        pred_arr.append(0)
        pred_arr.append(1)
    
    if curStat == 'Confirmed Case':
        pred_arr.append(1)
        pred_arr.append(0)
    else: 
        pred_arr.append(0)
        pred_arr.append(1)

    prediction = NB.get_prediction(pred_arr)
    prediction = prediction[0]

    if prediction[0]:
        if (prediction[0]).any():
            hosp = prediction[0]
            if prediction[0] <= 0 :
                hosp = 0
        if (prediction[2]).any():
            icu = prediction[2]
            if prediction[2] <= 0 :
                icu = 0
        if (prediction[4]).any():
            death = prediction[4]
            if prediction[4] <= 0 :
                death = 0

    return {'hosp': hosp, 'icu': icu, 'death': death}, 200

if __name__ == '__main__':
    app.run()