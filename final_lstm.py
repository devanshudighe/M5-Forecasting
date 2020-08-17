# -*- coding: utf-8 -*-
"""Final LSTM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16yiw1G0ZR0MYAynedDdHQpqLvGwvahwg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow.python.keras.layers import Dense,Dropout
from tensorflow.python.keras import Sequential
from tensorflow.keras.layers import LSTM
import datetime
from numpy import concatenate
from pandas import concat
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

from google.colab import drive
drive.mount('/content/drive')

sub3=pd.read_csv("/content/drive/My Drive/ML_257 Project/devanshu_submission_3.csv")
sub3.head()

sub2=pd.read_csv("/content/drive/My Drive/ML_257 Project/devanshu_submission_2.csv")
sub2.head()

sub1=pd.read_csv("/content/drive/My Drive/ML_257 Project/devanshu_submission_1.csv")
sub1.head()

sub2_sub3 = sub2.merge(sub3,right_index=True,left_index=True)
sub2_sub3.head()

dev_sub_123 = sub2_sub3.merge(sub1,right_index=True,left_index=True)
dev_sub_123.head()

pk_1=pd.read_csv("/content/drive/My Drive/ML_257 Project/0-2500.csv")

pk1_1 = pd.read_csv("/content/drive/My Drive/ML_257 Project/2500-3500.csv")

pk_sub1 = pk_1.merge(pk1_1,right_index=True,left_index=True)
pk_sub1.head()

dev_sub_4 = pd.read_csv("/content/drive/My Drive/devanshu_submission_1_1.csv")

sub0_6500= pk_sub1.merge(dev_sub_4,right_index=True,left_index=True)
sub0_6500.head()

sub6500_9500 = pd.read_csv("/content/drive/My Drive/ML_257 Project/submission_6500(sushant).csv")

sub0_9500 = sub0_6500.merge(sub6500_9500,right_index=True,left_index=True)
sub0_9500.head()

sub9500_12500 = pd.read_csv("/content/drive/My Drive/ML_257 Project/submission_1(sushant).csv")

sub12500_15500 = pd.read_csv("/content/drive/My Drive/ML_257 Project/submission_3(sushant).csv")
sub12500_15500.head()

sub9500_15500 = sub9500_12500.merge(sub12500_15500,right_index=True,left_index=True)
sub9500_15500.head()

sub0_15500 = sub0_9500.merge(sub9500_15500,right_index=True,left_index=True)
sub0_15500.head()

sub0_21500 = sub0_15500.merge(sub2_sub3,right_index=True,left_index=True)
sub0_21500.head()

sub21500_24500 = pd.read_csv("/content/drive/My Drive/ML_257 Project/21500-24500.csv")
sub21500_24500.head()

sub0_24500 = sub0_21500.merge(sub21500_24500,right_index=True,left_index=True)
sub0_24500.head()

sub0_27500 = sub0_24500.merge(sub1,right_index=True,left_index=True)
sub0_27500.head()

sub27500_28250 = pd.read_csv("/content/drive/My Drive/ML_257 Project/submission_lastvalues_1(sushant).csv")
sub28250_29000 = pd.read_csv("/content/drive/My Drive/ML_257 Project/submission_lastvalues_2(sushant).csv")
sub29000_29750 = pd.read_csv("/content/drive/My Drive/ML_257 Project/29000-29750.csv")
sub29750_30490 = pd.read_csv("/content/drive/My Drive/ML_257 Project/29750-30490.csv")

sub0_28250 = sub0_27500.merge(sub27500_28250,right_index=True,left_index=True)
 sub0_29000 = sub0_28250.merge(sub28250_29000,right_index=True,left_index=True)
 sub0_29750 = sub0_29000.merge(sub29000_29750,right_index=True,left_index=True)
 sub0_30490 = sub0_29750.merge(sub29750_30490,right_index=True,left_index=True)
 sub0_30490.head()

CAL_DTYPES={"event_name_1": "category", "event_name_2": "category", "event_type_1": "category", 
         "event_type_2": "category", "weekday": "category", 'wm_yr_wk': 'int16', "wday": "int16",
        "month": "int16", "year": "int16", "snap_CA": "float32", 'snap_TX': 'float32', 'snap_WI': 'float32' }

cal=pd.read_csv("/content/drive/My Drive/ML_257 Project/calendar.csv", header=0, dtype = CAL_DTYPES)
#cal=pd.read_csv("/home/014608347/m5_forecasting_g1/dataset/calendar.csv", header=0, dtype = CAL_DTYPES)
cal1 = cal
cal.head()

cal1["date"] = pd.to_datetime(cal1["date"])
for col, col_dtype in CAL_DTYPES.items():
  if col_dtype == "category":
    cal1[col] = cal1[col].cat.codes.astype("int16")
    cal1[col] -= cal1[col].min()

cal1.head()

is_train = True
nrows = None
first_day = 1
h = 28 
max_lags = 57
tr_last = 1913
fday = datetime.datetime(2011,1, 29) 
fday

start_day = max(1 if is_train  else tr_last-max_lags, first_day)
numcols = [f"d_{day}" for day in range(start_day,tr_last+1)]
catcols = ['id', 'item_id', 'dept_id','store_id', 'cat_id', 'state_id']
dtype = {numcol:"float32" for numcol in numcols} 
dtype.update({col: "category" for col in catcols if col != "id"})
dt = pd.read_csv("/content/drive/My Drive/ML_257 Project/sales_train_validation.csv", 
                  nrows = nrows, usecols = catcols + numcols, dtype = dtype)

dt.head()

dt = dt.drop(columns=["item_id","dept_id","cat_id","store_id","state_id"])
dt.head()

dt = dt.T
dt = dt.rename(columns=dt.iloc[0])
dt.head()

dt = dt.drop(labels="id", axis=0)
dt.head()

cal1 = cal1.iloc[:,6:]
cal1.head()

cal1 = cal1.set_index('d')
cal1.head()

result = pd.concat([dt, cal1], axis=1)
result.head()

result = result.iloc[:1913,:]
result.tail()

result.shape

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	agg=agg.fillna(0)
	return agg

reframed = series_to_supervised(result, 1, 1)
reframed.shape

reframed = reframed.iloc[:,:60987]

reframed.head()

#360 Days data.
one_yr_data=reframed.iloc[1793:1913,:]

def form_inputs(data, i):
  #loop for all the products
  orig = 'var'+str(i)+'(t-1)'
  pred = 'var'+str(i)+'(t)'
  one_prod = data[[orig,'var30491(t-1)','var30492(t-1)','var30493(t-1)','var30494(t-1)','var30495(t-1)','var30496(t-1)','var30497(t-1)',pred]].copy()
  values=one_prod.values
  return values

def split_sequences(sequences, n_steps):
	X, y = list(), list()
	for i in range(len(sequences)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the dataset
		if end_ix > len(sequences):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
		X.append(seq_x)
		y.append(seq_y)
	return np.array(X), np.array(y)

def LSTM_model(n_steps, n_features, X, y):
  model = Sequential()
  model.add(LSTM(30, activation='sigmoid', input_shape=(n_steps, n_features)))
  model.add(Dropout(0.3))
  model.add(Dense(30))
  model.compile(optimizer='adam', loss='mse')
  model.fit(X, y, epochs=50, verbose=0)
  return model

def test():
  lstm_pred = pd.DataFrame()
  for i in range(3500,6500):
    inp_values = form_inputs(one_yr_data, i+1)
    n_steps = 30
    # convert into input/output
    X, y = split_sequences(inp_values, n_steps)
    # the dataset knows the number of features, e.g. 2
    n_features = X.shape[2]
    X=X.astype(float)
    y=y.astype(float)
    model = LSTM_model(n_steps, n_features, X, y)
    X_test=inp_values[1883:1913,:-1].astype(float)
    X_test=X_test.reshape(1,30,8)
    yhat = model.predict(X_test, verbose=0)
    lstm_pred[result.columns[i]] = yhat.flatten()
  return lstm_pred

lstm_pred = test()
#lstm_pred.head()

lstm_pred.to_csv("/content/drive/My Drive/ML_257 Project/devanshu_submission_1.csv",index=False)



"""# Submission starts here"""

sub0_30490.head()

sample_sub = pd.read_csv("/content/drive/My Drive/ML_257 Project/sample_submission.csv")
sample_sub.shape

sub0_30490 = sub0_30490.T
sub0_30490.shape

sub0_30490_copy = sub0_30490.copy()

col_names = list()
#col_name.append('id')
for i in range(1,29):
  col_names.append('F'+str(i))

for i in range(0,30):
  sub0_30490_copy = sub0_30490_copy.rename(columns={i:'F'+str(i+1)})

sub0_30490_copy.head()

sub0_30490_copy.reset_index(level=0,inplace=True)
sub0_30490_copy.head()

sub0_30490_copy = sub0_30490_copy.rename(columns={'index':'id'})
sub0_30490_copy.head()

sub0_30490_final = sub0_30490_copy.iloc[:,:-2]
sub0_30490_final.shape

sub2 = sub0_30490_final.copy()
sub2["id"] = sub2["id"].str.replace("validation$", "evaluation")
sub0_30490_final_1 = pd.concat([sub0_30490_final, sub2], axis=0, sort=False)
sub0_30490_final_1.shape

sub0_30490_final_1.to_csv("/content/drive/My Drive/ML_257 Project/Group_1_Submission_1.csv",index=False)