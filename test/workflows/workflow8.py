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
async def returndegree(list) -> list:
        data1 = list[0]
        data2 = list[1]
        name, gender = data1[0]
        
        # Extract information from data2
        courses = []
        total_score = 0
        for item in data2:
            course_name = item[1]
            score = item[2]
            if score >= 60:
                courses.append(course_name)
            total_score += score
        passed_courses_count = len(courses)
        average_score = round(total_score / len(data2), 2)
        
        # Create the result list
        result = [name, gender, data2[0][0], passed_courses_count, average_score]
        
        

        # 返回搜索结果
        return result


# Temporal Workflow
@workflow.defn(sandboxed=False)
class RTWorkflow:
    @workflow.run
    async def run(self,list) -> list:
        
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    #

    # 解密密文 A 和 B
    
        privkey = rsa.PrivateKey.load_pkcs1(r.get('pr3'))
        cipher_a = list[0]
        cipher_b = list[1]
        result1 = base64.b64decode(cipher_a.encode('utf-8'))
        result2 = base64.b64decode(cipher_b.encode('utf-8'))
    
        result1 = rsa.decrypt(result1,privkey)
        result1 = eval(result1.decode('utf-8'))
        result2 = rsa.decrypt(result2,privkey)
        result2 = eval(result2.decode('utf-8'))

        list = []
        list.append(result1)
        list.append(result2)
        result = await workflow.execute_activity(
            returndegree,
            list,
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
    
    # 从 Redis 中获取密文 A 和 B
    cipher_a = r.get("A")
    cipher_b = r.get("B")
    print(cipher_a)
    print(cipher_b)




    # # Run a worker for the workflow
    # async with Worker(
    #     client,
    #     task_queue="datasearch-queue",
    #     workflows=[FindWorkflow],
    #     activities=[search_database],
    # ):

        # While the worker is running, use the client to run the workflow and
        # print out its result. Note, in many production setups, the client
        # would be in a completely separate process from the worker.
    list = []
    list.append(cipher_a)
    list.append(cipher_b)
    
    
    result = await client.execute_workflow(
        RTWorkflow.run,
        list,
        id=myid,
        task_queue="returndegree",
    )
    
    
    

    print(f"Result: {result}")
    
    
    

        


if __name__ == "__main__":
    asyncio.run(main())