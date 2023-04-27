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

# 定义workflow接口
with workflow.unsafe.sandbox_unrestricted():
    def read_file(path) -> bytes:

        with open(path, "rb") as handle:
            return handle.read()


@workflow.defn(sandboxed=False)
class FindWorkflow1:
    @workflow.run
    
    async def run(self, data) -> list:
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(host='localhost', port=6379, decode_responses=True) 
        privkey1 = rsa.PrivateKey.load_pkcs1(r.get('pr1'))
        data = str(rsa.decrypt(data, privkey1),encoding = "utf-8")
        
        result = await workflow.execute_activity(
            search_database1,
            data,
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        pubkey3 = rsa.PublicKey.load_pkcs1(r.get('pu3'))
        result = rsa.encrypt(str(result).encode('utf-8'),pubkey3)
        print(result)
        return result
        # workflow.logger.info("Result: %s", result)
        
@workflow.defn(sandboxed=False)
class FindWorkflow2:
    @workflow.run
    async def run(self, data) -> list:
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(host='localhost', port=6379, decode_responses=True) 
     
        privkey2 = rsa.PrivateKey.load_pkcs1(r.get('pr2'))
        data = str(rsa.decrypt(data, privkey2),encoding = "utf-8")
        result = await workflow.execute_activity(
            search_database2,
            data,
            start_to_close_timeout=timedelta(seconds=10),
        )
        pubkey3 = rsa.PublicKey.load_pkcs1(r.get('pu3'))
        result = rsa.encrypt(str(result).encode('utf-8'),pubkey3)
        print(result)
        return result


# 定义activity接口
@activity.defn
async def search_database1(data) -> list:
     # 从本地数据库中查找符合的数据
        print('1')
        
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='11911707',
            database='50q'     
        )
        cursor = conn.cursor()
        print(data)
        query = f"select SNAME, SSEX from STUDENT where SNO= {data}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        print(result)

        logging.info(f"Found {len(result)} records matching the search criteria.")

        # 返回搜索结果
        return result
    
@activity.defn
async def search_database2(data) -> list:
     # 从本地数据库中查找符合的数据
        print('2')
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='11911707',
            database='50q'     
        )
        cursor = conn.cursor()
        query = f"select * from SCORE where SNO= {data};"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        result = tuple(tuple(float(x) if isinstance(x, decimal.Decimal) else x for x in tpl) for tpl in result)
        print(result)

        logging.info(f"Found {len(result)} records matching the search criteria.")

        # 返回搜索结果
        return result



async def main():
    # Uncomment the line below to see logging
    # logging.basicConfig(level=logging.INFO)

    # Start client

    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
   

    client = await Client.connect("localhost:7233")



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
        
    
    with open('pubkey1.pem') as f:
        pubkey1 = rsa.PublicKey.load_pkcs1(f.read().encode())
    with open('pubkey2.pem') as f:
        pubkey2 = rsa.PublicKey.load_pkcs1(f.read().encode())
    with open('pubkey3.pem') as f:
        pubkey3 = rsa.PublicKey.load_pkcs1(f.read().encode())

    myid = str(random.randrange(1,99999))
    string = '101'
    string1 = rsa.encrypt(string.encode('utf-8'), pubkey1)
    string2 = rsa.encrypt(string.encode('utf-8'), pubkey2)
    print(type(string))
    result1 = await client.execute_workflow(
        FindWorkflow1.run,
        string1,
        id=myid,
        task_queue="datasearchqueue",
    )
    result2 = await client.execute_workflow(
        FindWorkflow2.run,
        string2,
        id=myid,
        task_queue="datasearchqueue",
    )
    
    
    print(f"Result2: {result1}")
    print(f"Result1: {result2}")
    privkey3 = rsa.PrivateKey.load_pkcs1(r.get('pr3'))
    
  
    
    print(result1)
    print(result2)
    r.delete('A')
    r.delete('B')
    
    #二进制编码后储存
    encoded_ciphertext = base64.b64encode(result1).decode('utf-8')
    r.set('A', encoded_ciphertext)
    
    encoded_ciphertext = base64.b64encode(result2).decode('utf-8')
    r.set('B', encoded_ciphertext)
    
    result1 = r.get('A')
    result2 = r.get('B')
    
    encoded_ciphertext1 = r.get('A')
    encoded_ciphertext2 = r.get('B')
    
    result1 = base64.b64decode(encoded_ciphertext1.encode('utf-8'))
    result2 = base64.b64decode(encoded_ciphertext2.encode('utf-8'))
    
    result1 = rsa.decrypt(result1,privkey3)
    result1 = eval(result1.decode('utf-8'))
    result2 = rsa.decrypt(result2,privkey3)
    result2 = eval(result2.decode('utf-8'))
    
    print(result1)
    print(result2)
        


if __name__ == "__main__":
    asyncio.run(main())