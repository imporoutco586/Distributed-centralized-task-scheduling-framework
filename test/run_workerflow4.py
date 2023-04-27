import asyncio
import random
import string
from temporalio.client import Client
#Load training data and test data from csv files
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Import the workflow from the previous code
from workflows.workflow2 import say_hello_workflow
from workflows.workflow4 import trainreturnflow,testreturnflow

task_queue = "say-hello-task-queue"
# workflow_name = say-hello-workflow
activity_name = "say-hello-activity"
workflow_id = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=30)
        )



async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # # Execute a workflow
    print(f"My id is {workflow_id}")
    # result = await client.execute_workflow(say_hello_workflow.run, "Temporal", id=workflow_id, task_queue=task_queue)

    # print(f"Result: {result}")
  
    # regr = linear_model.LinearRegression()
    # #Load test data
    # test_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/test.csv')
    # test_data.dropna(inplace=True)


    train_data = await client.execute_workflow(trainreturnflow.run, id=workflow_id, task_queue="train-queue")
    test_data = await client.execute_workflow(testreturnflow.run, id=workflow_id, task_queue="test-queue")
#Train the model using the training sets


    # test_data = await client.execute_workflow(trainreturnflow.run, id=workflow_id, task_queue="ml-queue")
    # #Load test data
    # test_data = pd.read_csv('/home/imporoutco/Desktop/ts/test/ml/test.csv')
    # test_data.dropna(inplace=True)

    regr = linear_model.LinearRegression()
 

    #Train the model using the training sets
    regr.fit(np.array(train_data[0]).reshape((-1, 1)), train_data[1])

    #Make predictions using the validation data
    #Make predictions using the validation data
    y_pred = regr.predict(np.array(test_data[0]).reshape((-1, 1)))

    #The coefficients
    print('Coefficients: ', regr.coef_)
    #The mean squared error
    print('Mean squared error: %.2f' % mean_squared_error(test_data[1], y_pred))
    #The coefficient of determination: 1 is perfect prediction
    print('Coefficient of determination: %.2f' % r2_score(test_data[1], y_pred))
    #The coefficients
   

    #Plot outputs
    plt.scatter(test_data[0], test_data[1], color='black')
    plt.plot(test_data[0], y_pred, color='blue', linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()

    

if __name__ == "__main__":
    asyncio.run(main())




