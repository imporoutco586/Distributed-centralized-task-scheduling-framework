from temporalio import activity
#Load training data and test data from csv files
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


@activity.defn
async def returntrain ():
    train_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/train.csv')
    train_data.dropna(inplace=True)
    list=[]
    list.append(train_data['x'])
    list.append(train_data['y'])
    return list

@activity.defn
async def returntest ():
    test_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/test.csv')
    test_data.dropna(inplace=True)
    list1=[]
    list1.append(test_data['x'])
    list1.append(test_data['y'])
    return list1