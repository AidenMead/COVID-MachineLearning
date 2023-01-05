import requests
import pandas as pd

# A helped function just to hit the CDC endpoint to request the data. We expect the parameters for the 
# CDC request to be provided (can be an empty dict).
def get_cdc_data(params):
    URL = 'https://data.cdc.gov/resource/n8mc-b4w4.json'
    data = requests.get(URL, params)
    json = data.json()
    dataframe = pd.DataFrame(json)
    return dataframe

# Handles creating the filters to only pull relevant data - no missing data or incomplete records. This 
# allows the learning algorithm to ensure accuracy. After building filters, it uses the above function 
# to query to CDC API and passes the filter data to the function. 
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
    df = get_cdc_data('$where='+filter_obj['age']+ ' AND '+filter_obj['sex']+ ' AND '+filter_obj['comorbidity']+ ' AND '+filter_obj['symptoms']+ ' AND '+filter_obj['hosp']+ ' AND '+filter_obj['death']+ ' AND '+filter_obj['icu']+' AND '+filter_obj['current']+'&$limit=500000')
    return df

# Creates a single instance of the clean data to prevent continuous querying between building the 
# algorithm and creating the data for the visualizations.
single_df = cleaned_dataframe()

# Handles the structuring of the data for the visualizations. This is taking the current dataframe, 
# stripping down to only necessary columns, and then assigning the relevant data to specific keys 
# to be consumed by the frontend for dynamic visualization rendering. 
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
