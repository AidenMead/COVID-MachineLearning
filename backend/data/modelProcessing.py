from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.model_selection import train_test_split
import numpy
import pandas as pd
import data.dataSource as ds

# This code is the heart of the machine learning - this pulls the clean dataframe that was grathered from the CDC site,
# drops the unnecessary columns, then splits the existing columns into binary columns (ex: splits age_group column which 
# could have 4 values into 4 columns with a binary value to singal if that value is assigned to the record). Once the 
# data is ready, if splits the data into the independent and dependent columns, then partitions the data into a training 
# group and testing group. 
# 
# Finally, we use Bayesian Ridge algorithm wrapped in a MultiOutput Regressor. The Bayesian Ridge 
# gives us the machine learning process method and the MultiOutput Regressor allows the code to address each possible 
# output variable independently to allow multiple predictions at once. 
# 
# Once the model is trailed and assigned to the MOR value, we can then create a function that can be called at will 
# for use when the API endpoint is hit during a request from the front end for a prediction.

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
