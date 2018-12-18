# -*- coding: utf-8 -*-
"""Copy of Stock_Market_Analysis (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19I2xi0zTga0lJ5e_GMr26ex0HdNUAmoF

# Stock Market Analysis

### Problem Link : https://www.kaggle.com/daiearth22/uniqlo-fastretailing-stock-price-prediction/data

#### Necessary Import Statements
"""

import pandas as pd
import numpy as np
# %matplotlib inline
from matplotlib import pyplot as plt
from pandas import Series
from pandas import DataFrame
from pandas import concat

# Train test split
from sklearn.model_selection import TimeSeriesSplit


# Models
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestRegressor

# Model evaluators
from sklearn.metrics import f1_score,confusion_matrix

"""### Reading the Train Data"""

!wget https://www.dropbox.com/s/22nfk89c8hshxhs/Train.csv

train = pd.read_csv("Train.csv")
train.info()

train.head()

train['Avg'] = train['Stock Trading'] / train['Volume']

train.describe()

train.head()

train.tail()

train['Open'].plot(color='k')

train.head()

"""Seperating the DateTime field to data, month and year into different columns."""

train['Year'] = pd.DatetimeIndex(train['Date']).year
train['Month'] = pd.DatetimeIndex(train['Date']).month
train['Day'] = pd.DatetimeIndex(train['Date']).day

train.head()

"""Function for dropping of unnecesary features or redundant features"""

def drop_features(features,data):
    data.drop(features,inplace=True,axis=1)

drop_features(['Date'],train)

"""### Applying the TimeSeries Feature Engineering
#### Lag Features
"""

train.info()

open_vals = Series(train['Open'])

open_vals.head()

open_vals.shift(-1).head()

open_vals.shift(-1).tail()

#Applying Lag Features to Opening Price
open1 = Series(train['Open'])
open_dataframe = concat([open1.shift(-3), open1.shift(-2), open1.shift(-1)], axis=1)
open_dataframe.columns = ['O_t-3', 'O_t-2', 'O_t-1']
open_dataframe.shape

open_dataframe.head()

#combining the train data and the lag features of Temp
train1 = pd.concat([train, open_dataframe], axis=1)

train1.head()

train1.tail()

#Applying Lag Features to Opening Price
close_vals = Series(train['Close'])
close_dataframe = concat([close_vals.shift(-3), close_vals.shift(-2), close_vals.shift(-1)], axis=1)
close_dataframe.columns = ['C_t-3', 'C_t-2', 'C_t-1']
close_dataframe.shape

#combining the train data and the lag features of Temp
train1 = pd.concat([train1, close_dataframe], axis=1)

train1.head()

train1.tail()

#dropping null value rows
train1.dropna(inplace = True)

train1.tail()

train1.shape

#since for combining of data, both should have same number of rows. hence, removing the extra row
#train1.drop(train1.head(1).index, inplace=True)
#train1.shape

"""#### Rolling Window Statistics"""

# Appling window Features for the Highest Value Feature
high = train['High']
w = 5

shift = high.shift(-w+1)

train['High'].head(8)

shift.head(8)

shift.head()

window = shift.rolling(window=w)

type(window)

window.min().head()

window.min()

window.min().tail(50)

df = concat([window.min(), window.mean(), window.max()], axis=1)
df.columns = ['min', 'mean', 'max']



df.head(10)



#combining the train1 and the rolling window features
train2 = pd.concat([train1, df], axis=1)

train2.head()

train2.tail()

"""#### Expanding window Statistics"""

train2.dropna(inplace=True)

train2.head()

#Applying Expanding window for the Lowest Value
low= train['Low']
window = low.expanding(5)
dfc = concat([window.min(), window.mean(), window.max()], axis=1)
dfc.columns = ['min', 'mean', 'max']

#no null values
dfc.shape

#to make it equal to the train2, dropping forst 4 values
#dfc.drop(dfc.head(4).index, inplace=True)

dfc.shape

#concating the expanding window features to the previous train2.
train_final = pd.concat([train2, dfc], axis=1)

train_final.tail()

#Replacing the null values with -1 if any.
train_final.dropna(inplace = True)

#Complete final Train Data
train_final.shape

train_final.drop('High',axis=1,inplace=True)
train_final.drop('Low',axis=1,inplace=True)
train_final.drop('Open',axis=1,inplace=True)

"""### Splitting of Data"""

from sklearn.model_selection import train_test_split

train_final.info()

train_final.drop(['Avg'],axis=1,inplace=True)

train_final.info()

X_train,X_test,y_train,y_test = train_test_split(train_final.drop('Close',axis=1)
                                                 ,train_final['Close'],random_state=42)

X_train.head()

"""### Applying Regressor Model"""

model=RandomForestRegressor()

model.fit(X_train,y_train)

predict=model.predict(X_test)

model.feature_importances_

imp_list = list(model.feature_importances_)

col_lis = list(X_test.columns)

feature_importances = {i[0]:"{0:.4f}".format(i[1]) for i in list(zip(col_lis,imp_list))}

feature_importances

"""#### Measuring the Score. (Evaluation Metrics)"""

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predict))
print('MSE:', metrics.mean_squared_error(y_test, predict))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predict)))

from sklearn.cross_validation import cross_val_score

print(cross_val_score(model, X_test, y_test,cv=5))
