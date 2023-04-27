import os
import json
import logging
from typing import Dict, Any
import asyncio
from datetime import timedelta
import random
import string
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

import mysql.connector
# -*- coding: utf-8 -*-

# 定义workflow接口
@workflow.defn
class FindWorkflow:
    @workflow.run
    async def run(self, data) -> list:
        result = await workflow.execute_activity(
            search_database,
            data,
            start_to_close_timeout=timedelta(seconds=10),
        )
        print(result)
        return result
        # workflow.logger.info("Result: %s", result)


# 定义activity接口
@activity.defn
async def search_database(data) -> list:
     # 从本地数据库中查找符合的数据
        print('1')
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='11911707',
            database='50q'     
        )
        cursor = conn.cursor()
        query = f"select SNAME from {data}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        print(result)

        logging.info(f"Found {len(result)} records matching the search criteria.")

        # 返回搜索结果
        return result


# workflow_id = "".join(
#         random.choices(string.ascii_uppercase + string.digits, k=30)
#     )      


async def main():
    # Uncomment the line below to see logging
    # logging.basicConfig(level=logging.INFO)

    # Start client
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
    string = 'STUDENT'
    print(type(string))
    result = await client.execute_workflow(
        FindWorkflow.run,
        string,
        id='11239135',
        task_queue="datasearchqueue",
    )
    print(f"Result: {result}")
        


if __name__ == "__main__":
    asyncio.run(main())