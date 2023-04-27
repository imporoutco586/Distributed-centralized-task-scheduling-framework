#Load training data and test data from csv files
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

#Load training data
train_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/train.csv')
train_data.dropna(inplace=True)
#Load test data
test_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/test.csv')
test_data.dropna(inplace=True)

#Split training data into training and validation data
train, validation = train_test_split(train_data, test_size=0.2)

#Create linear regression object
regr = linear_model.LinearRegression()

#Train the model using the training sets
regr.fit(train[['x']], train['y'])

#Make predictions using the validation data
y_pred = regr.predict(validation[['x']])
#The coefficients
print('Coefficients: ', regr.coef_)
#The mean squared error
print('Mean squared error: %.2f' % mean_squared_error(validation['y'], y_pred))
#The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f' % r2_score(validation['y'], y_pred))

#Plot outputs
plt.scatter(validation['x'], validation['y'], color='black')
plt.plot(validation['x'], y_pred, color='blue', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

#Make predictions using the test data
y_pred = regr.predict(test_data[['x']])
#Save the predictions to a csv file
pd.DataFrame({'x': test_data['x'], 'y': y_pred}).to_csv('linear.csv', index=False)
