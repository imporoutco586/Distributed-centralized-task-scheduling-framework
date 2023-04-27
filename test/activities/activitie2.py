from temporalio import activity
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

@activity.defn
async def trainmodel(regr) :
    train_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/train.csv')
    train_data.dropna(inplace=True)
    #Load test data
    test_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/test.csv')
    test_data.dropna(inplace=True)

    #Split training data into training and validation data
    train, validation = train_test_split(train_data, test_size=0.2)

    #Create linear regression object
    regr = linear_model.LinearRegression()

    
    regr.fit(train_data[['x']], train_data['y'])

    return regr

    # #Make predictions using the test_data data
    # y_pred = regr.predict(test_data[['x']])
    # #The coefficients
    # print('Coefficients: ', regr.coef_)
    # #The mean squared error
    # print('Mean squared error: %.2f' % mean_squared_error(test_data['y'], y_pred))
    # #The coefficient of determination: 1 is perfect prediction
    # print('Coefficient of determination: %.2f' % r2_score(test_data['y'], y_pred))