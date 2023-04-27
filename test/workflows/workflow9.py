import os
import json
import logging
from typing import Dict, Any
import asyncio
from datetime import timedelta

import rsa
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

import mysql.connector
with workflow.unsafe.imports_passed_through():
    import random
    import string
    import redis
    import platform 
    import decimal
    import base64
    import redis
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score
    import pandas as pd
    import numpy as np  
    from sklearn.preprocessing import StandardScaler

    from sklearn.model_selection import GridSearchCV
    import pickle
    import json
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
# -*- coding: utf-8 -*-


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

PRIVATE_KEY_FILE = "private_key.pem"


# 从 Redis 中获取密文 A 和 B，并解密
# def get_decrypted_data() -> Tuple[Tuple[str, str], Tuple[str, str, List[int]]]:
#     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

#     # 从 Redis 中获取密文 A 和 B
#     cipher_a = r.get("A")
#     cipher_b = r.get("B")

#     # 解密密文 A 和 B
    
#     privkey = rsa.PrivateKey.load_pkcs1(r.get('pr3'))

#     data_a = rsa.decrypt(cipher_a, privkey, "utf-8")
#     data_b = rsa.decrypt(cipher_b, privkey, "utf-8")
    
    

#     # 将解密后的数据转换成元组返回
#     return tuple(eval(data_a)), tuple(eval(data_b))




@activity.defn
async def returntrain1() -> str:
        X_train1 = np.load('X_train1.npy')
        y_train1 = np.load('y_train1.npy')
        rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        rf_classifier.fit(X_train1, y_train1)

        
        with open('rf_model.pkl', 'wb') as f:
            pickle.dump(rf_classifier, f)
    
        with open('rf_model.pkl', 'rb') as f:
            model_str = f.read()
        
        

        # 返回搜索结果
        return model_str


# Temporal Workflow
@workflow.defn(sandboxed=False)
class Train1Workflow:
    @workflow.run
    async def run(self) -> str:
       


        result = await workflow.execute_activity(
            returntrain1,
      
            start_to_close_timeout=timedelta(seconds=10),
        )

 

        # 返回结果
        return result
    

@activity.defn
async def returntrain2(model_str) -> str:
    X_train2 = np.load('X_train2.npy')
    y_train2 = np.load('y_train2.npy')

    with open('rf_model.pkl', 'wb') as f:
        f.write(model_str)
    
    with open('rf_model.pkl', 'rb') as f:
        rf_loaded = pickle.load(f)
        
        rf_loaded.fit(X_train2, y_train2)

        
    with open('rf_loaded.pkl', 'wb') as f:
        pickle.dump(rf_loaded, f)
    
    with open('rf_loaded.pkl', 'rb') as f:
        model_str = f.read()
        
        

        # 返回搜索结果
    return model_str


# Temporal Workflow
@workflow.defn(sandboxed=False)
class Train2Workflow:
    @workflow.run
    async def run(self,model_str) -> str:
        


        result = await workflow.execute_activity(
            returntrain2,
            model_str,
  
            start_to_close_timeout=timedelta(seconds=10),
        )

 

        # 返回结果
        return result

async def main():
    # Uncomment the line below to see logging
    # logging.basicConfig(level=logging.INFO)

    # Start client

    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
   

    client = await Client.connect("localhost:7233")
    myid = str(random.randrange(1,99999))
    
    
    # Load the dataset
    data = pd.read_csv('/home/zky/Desktop/ts/HW2_2_data.csv')

    # Data preprocessing
    # TODO: data preprocessing code
    print(data.isnull().sum())

    # Delete missing values
    data = data.dropna()

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data[['x1', 'x2', 'x3']], data['class'], test_size=0.2, random_state=42)

    #  Feature scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # X_train1, X_train2, y_train1, y_train2 = train_test_split(X_train, y_train, test_size=0.6, random_state=42)
    
    # np.save('X_train1.npy',X_train1)
    # np.save('X_train2.npy',X_train2)
    # np.save('y_train1.npy',y_train1)
    # np.save('y_train2.npy',y_train2)

    
    result1 = await client.execute_workflow(
        Train1Workflow.run,
        id=myid,
        task_queue="train1",
    )
    
    string = result1
    
    with open('rf_model1.pkl', 'wb') as f:
        f.write(result1)
    
    with open('rf_model1.pkl', 'rb') as f:
        result1 = pickle.load(f)
    
    rf_predictions = result1.predict(X_test)


# 计算随机森林分类器的准确性
    rf_accuracy = accuracy_score(y_test, rf_predictions)
    
    print(f"随机森林分类器的准确性为：{rf_accuracy:.3f}")
    
    result2 = await client.execute_workflow(
        Train2Workflow.run,
        string,
        id=myid,
        task_queue="train2",
    )
    
    with open('rf_model2.pkl', 'wb') as f:
        f.write(result2)
    
    with open('rf_model2.pkl', 'rb') as f:
        result2 = pickle.load(f)
    
    rf_predictions = result2.predict(X_test)


# 计算随机森林分类器的准确性
    rf_accuracy = accuracy_score(y_test, rf_predictions)
    
    print(f"随机森林分类器的准确性为：{rf_accuracy:.3f}")
    
    
    

        


if __name__ == "__main__":
    asyncio.run(main())