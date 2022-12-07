from sklearn.naive_bayes import BernoulliNB
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import BayesianRidge
import numpy
import pandas as pd
from sklearn.model_selection import train_test_split
import data.dataSource as ds
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score, confusion_matrix

df = ds.cleaned_dataframe()
df = df.loc[:,['age_group','sex','underlying_conditions_yn','symptom_status', 'current_status','hosp_yn','icu_yn', 'death_yn']]

df = pd.get_dummies(df)

X = df.drop(['hosp_yn_Yes', 'hosp_yn_No', 'icu_yn_Yes', 'icu_yn_No', 'death_yn_Yes', 'death_yn_No'], axis=1).to_numpy()
y = df.loc[:, ['hosp_yn_Yes', 'hosp_yn_No', 'icu_yn_Yes', 'icu_yn_No', 'death_yn_Yes', 'death_yn_No']].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=1234)

nb = BayesianRidge()
nb = MultiOutputRegressor(nb)

nb.fit(X_train, y_train)

sample = numpy.array([0,0,0,1,0,1,0,1,0,1,1]).reshape(1,-1)
y_pred = nb.predict(X_test)

def get_prediction(datapoints):
    datapoints = numpy.array(datapoints).reshape(1,-1)
    pred = nb.predict(datapoints)
    return pred
