import requests
import pandas as pd

def get_cdc_data(params):
    URL = 'https://data.cdc.gov/resource/n8mc-b4w4.json'
    data = requests.get(URL, params)
    json = data.json()
    return json

def get_data_as_dataframe(params={}):
    json = get_cdc_data(params)
    dataframe = pd.DataFrame(json)
    return dataframe

def cleaned_dataframe():
    filter_obj = {
        'age': 'age_group not in("Unknown", "Missing", "NA")',
        'sex': 'sex in("Male", "Female")',
        'comorbidity': 'underlying_conditions_yn in("Yes", "No")',
        'symptoms': 'symptom_status not in("Unknown", "Missing")',
        'current': 'current_status not in ("Unknown", "Missing")',
        'hosp': 'hosp_yn in("Yes","No")',
        'death': 'death_yn in("Yes", "No")',
        'icu': 'icu_yn in("Yes", "No")'
    }
    df = get_data_as_dataframe('$where='+filter_obj['age']+ ' AND '+filter_obj['sex']+ ' AND '+filter_obj['comorbidity']+ ' AND '+filter_obj['symptoms']+ ' AND '+filter_obj['hosp']+ ' AND '+filter_obj['death']+ ' AND '+filter_obj['icu']+' AND '+filter_obj['current']+'&$limit=500000')
    return df

single_df = cleaned_dataframe()

def get_demographic_rates():
    df = single_df
    df = df.loc[:, ['symptom_status', 'sex', 'age_group', 'current_status','underlying_conditions_yn', 'hosp_yn', 'icu_yn', 'death_yn']]

    def findEventNumbers(demog, demogState, humanReadableDemogName):
        def getValue(event):
            try: 
                return df.groupby(demog)[event].value_counts()[demogState]['Yes']
            except: 
                return 0
    
        total = df[demog].value_counts()[demogState] 
        hosp =  getValue('hosp_yn')
        icu  = getValue('icu_yn')
        death = getValue('death_yn')

        mild = total - hosp - icu - death
        return {
            'demographic': humanReadableDemogName,
            'total_count': int(total),
            'hospitalized': int(hosp),
            'icu': int(icu),
            'death': int(death),
            'mild': int(mild)
        }


    mapping = {
        'total_counts': {
            'all': int(df[df.columns[0]].count()),
            'hospitalized': int(df['hosp_yn'].value_counts()['Yes']),
            'icu': int(df['icu_yn'].value_counts()['Yes']),
            'death': int(df['death_yn'].value_counts()['Yes'])
        },
        'values_arr': {
        'comorbidity':[
            findEventNumbers('underlying_conditions_yn', 'Yes', 'Comorbidities'),
            findEventNumbers('underlying_conditions_yn', 'No', 'No Comorbidities'),
            ], 
        'symptomatic':[
            findEventNumbers('symptom_status', 'Asymptomatic', 'Asymptomatic'),
            findEventNumbers('symptom_status', 'Symptomatic', 'Symptomatic'),
            ],
        'ages':[
            findEventNumbers('age_group', '0 - 17 years','0-17 Yrs'),
            findEventNumbers('age_group', '18 to 49 years','18-49 Yrs'),
            findEventNumbers('age_group', '50 to 64 years','50-64 Yrs'),
            findEventNumbers('age_group', '65+ years','65+ Yrs'),
            ],
        'covid_status': [
            findEventNumbers('current_status', 'Laboratory-confirmed case', 'Confirmed'),
            findEventNumbers('current_status', 'Probable Case', 'Probable')
        ],
        'sex':[
            findEventNumbers('sex', 'Male', 'Male'),
            findEventNumbers('sex', 'Female', 'Female')
        ]
        }
    }

    return mapping
