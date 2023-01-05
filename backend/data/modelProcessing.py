from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split
import numpy
import pandas as pd
import data.dataSource as ds

df = ds.single_df
df = df.loc[:,['age_group','sex','underlying_conditions_yn','symptom_status', 'current_status','hosp_yn','icu_yn', 'death_yn']]

df = pd.get_dummies(df)

X = df.drop(['hosp_yn_Yes', 'hosp_yn_No', 'icu_yn_Yes', 'icu_yn_No', 'death_yn_Yes', 'death_yn_No'], axis=1).to_numpy()
y = df.loc[:, ['hosp_yn_Yes', 'hosp_yn_No', 'icu_yn_Yes', 'icu_yn_No', 'death_yn_Yes', 'death_yn_No']].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=1234)

br = BayesianRidge()
mor = MultiOutputRegressor(br)

mor.fit(X_train, y_train)

def get_prediction(datapoints):
    datapoints = numpy.array(datapoints).reshape(1,-1)
    pred = mor.predict(datapoints)
    return pred
