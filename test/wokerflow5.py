import diskcache
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

    # Execute a workflow
    print(f"My id is {workflow_id}")


    with open('pubkey1.pem') as f:
        pubkey1 = rsa.PublicKey.load_pkcs1(f.read().encode())

    with open('privkey1.pem') as f:
        privkey1 = rsa.PrivateKey.load_pkcs1(f.read().encode())
    with open('pubkey1.pem') as f:
        pubkey2 = rsa.PublicKey.load_pkcs1(f.read().encode())

    with open('privkey1.pem') as f:
        privkey2 = rsa.PrivateKey.load_pkcs1(f.read().encode())
    with open('pubkey1.pem') as f:
        pubkey3 = rsa.PublicKey.load_pkcs1(f.read().encode())

    with open('privkey1.pem') as f:
        privkey3 = rsa.PrivateKey.load_pkcs1(f.read().encode())

    number = 5

    result = await client.execute_workflow(say_hello_workflow.run, number, id=workflow_id, task_queue=task_queue)

    print(f"Result: {result}")
    print(f"input your number: ")
    number = str(input())
    result = await client.execute_workflow(encodeflow.run,number, id=workflow_id, task_queue="encode-queue")

    print(f"Result: {result}")
    print(f"input your number: ")
    number = str(input())
    
    result = await client.execute_workflow(decodeflow.run, number, id=workflow_id, task_queue="decode-queue")

    print(f"Result: {result}")


   



    

if __name__ == "__main__":
    asyncio.run(main())




