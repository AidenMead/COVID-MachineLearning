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
    df = get_data_as_dataframe('$where='+filter_obj['age']+ ' AND '+filter_obj['sex']+ ' AND '+filter_obj['comorbidity']+ ' AND '+filter_obj['symptoms']+ ' AND '+filter_obj['hosp']+ ' AND '+filter_obj['death']+ ' AND '+filter_obj['icu']+' AND '+filter_obj['current']+'&$limit=10000')
    return df

def get_demographic_rates():
    df = cleaned_dataframe()
    df = df.loc[:, ['symptom_status', 'sex', 'age_group', 'current_status','underlying_conditions_yn', 'hosp_yn', 'icu_yn', 'death_yn']]

    mapping = {
        'total_counts': int(df[df.columns[0]].count()),
        'values_arr': {
        'comorbidity':[{
            'demographic': 'Comorbidities',
            'total_count': int(df['underlying_conditions_yn'].value_counts()['Yes']),
            'hospitalized': int(df.groupby('underlying_conditions_yn')['hosp_yn'].value_counts()['Yes']['Yes']),
            'icu': int(df.groupby('underlying_conditions_yn')['icu_yn'].value_counts()['Yes']['Yes']),
            'death': int(df.groupby('underlying_conditions_yn')['death_yn'].value_counts()['Yes']['Yes']),
        },
        {
            'demographic': 'No Comorbidities',
            'comorbidity_n': int(df['underlying_conditions_yn'].value_counts()['No']),
            'hospitalized': int(df.groupby('underlying_conditions_yn')['hosp_yn'].value_counts()['No']['Yes']),
            'icu': 0,
            'death': 0,
        },], 
        'symptomatic':[{
            'demographic': 'Asymptomatic',
            'total_count': int(df['symptom_status'].value_counts()['Asymptomatic']),
            'hospitalized': int(df.groupby('symptom_status')['hosp_yn'].value_counts()['Asymptomatic']['Yes']),
            'icu': int(df.groupby('symptom_status')['icu_yn'].value_counts()['Asymptomatic']['Yes']),
            'death': int(df.groupby('symptom_status')['death_yn'].value_counts()['Asymptomatic']['Yes']),
        },
        {
            'demographic': 'Symptomatic',
            'total_count': int(df['symptom_status'].value_counts()['Symptomatic']),
            'hospitalized': int(df.groupby('symptom_status')['hosp_yn'].value_counts()['Symptomatic']['Yes']),
            'icu': int(df.groupby('symptom_status')['icu_yn'].value_counts()['Symptomatic']['Yes']),
            'death': int(df.groupby('symptom_status')['death_yn'].value_counts()['Symptomatic']['Yes']),
        },],
        'ages':[{
            'demographic': '0 to 17 years',
            'total_count': int(df['age_group'].value_counts()['0 - 17 years']),
            'hospitalized': int(df.groupby('age_group')['hosp_yn'].value_counts()['0 - 17 years']['Yes']),
            'icu': int(df.groupby('age_group')['icu_yn'].value_counts()['0 - 17 years']['Yes']),
            'death': 0,
        },
        {
            'demographic': '18 to 49 years',
            'total_count': int(df['age_group'].value_counts()['18 to 49 years']),
            'hospitalized': int(df.groupby('age_group')['hosp_yn'].value_counts()['18 to 49 years']['Yes']),
            'icu': int(df.groupby('age_group')['icu_yn'].value_counts()['18 to 49 years']['Yes']),
            'death': 0,
        },
        {
            'demographic': '50 to 64 years',
            'total_count': int(df['age_group'].value_counts()['50 to 64 years']),
            'hospitalized': int(df.groupby('age_group')['hosp_yn'].value_counts()['50 to 64 years']['Yes']),
            'icu': int(df.groupby('age_group')['icu_yn'].value_counts()['50 to 64 years']['Yes']),
            'death': 0,
        },
        {
            'demographic': '65+ years',
            'total_count': int(df['age_group'].value_counts()['65+ years']),
            'hospitalized': int(df.groupby('age_group')['hosp_yn'].value_counts()['65+ years']['Yes']),
            'icu': int(df.groupby('age_group')['icu_yn'].value_counts()['65+ years']['Yes']),
            'death': int(df.groupby('age_group')['death_yn'].value_counts()['65+ years']['Yes']),
        },],
        'covid_status': [{
            'demographic': 'Confirmed',
            'total_count': int(df['current_status'].value_counts()['Laboratory-confirmed case']),
            'hospitalized': int(df.groupby('current_status')['hosp_yn'].value_counts()['Laboratory-confirmed case']['Yes']),
            'icu': int(df.groupby('current_status')['icu_yn'].value_counts()['Laboratory-confirmed case']['Yes']),
            'death': int(df.groupby('current_status')['death_yn'].value_counts()['Laboratory-confirmed case']['Yes']),
        },
        {
            'demographic': 'Probable',
            'total_count': int(df['current_status'].value_counts()['Probable Case']),
            'hospitalized': int(df.groupby('current_status')['hosp_yn'].value_counts()['Probable Case']['Yes']),
            'icu': int(df.groupby('current_status')['icu_yn'].value_counts()['Probable Case']['Yes']),
            'death': int(df.groupby('current_status')['death_yn'].value_counts()['Probable Case']['Yes']),
        },],
        'sex':[{
            'demographic': 'Male',
            'total_count': int(df['sex'].value_counts()['Male']),
            'hospitalized': int(df.groupby('sex')['hosp_yn'].value_counts()['Male']['Yes']),
            'icu': int(df.groupby('sex')['icu_yn'].value_counts()['Male']['Yes']),
            'death': int(df.groupby('sex')['death_yn'].value_counts()['Male']['Yes']),
        },
        {
            'demographic': 'Female',
            'total_count': int(df['sex'].value_counts()['Female']),
            'hospitalized': int(df.groupby('sex')['hosp_yn'].value_counts()['Female']['Yes']),
            'icu': int(df.groupby('sex')['icu_yn'].value_counts()['Female']['Yes']),
            'death': int(df.groupby('sex')['death_yn'].value_counts()['Female']['Yes']),
        }]
        }
    }

    return mapping

def get_heatmap_data():
    # map for list [row, col, %]
    list = []
    i=0

    return True
