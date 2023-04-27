import asyncio
import random
import string

from temporalio.client import Client
from temporalio.worker import Worker
import sys
sys.path.append('..')
# Import the activity and workflow from our other files
from  activities.activitie1 import encode
from  workflows.workflow3 import encodeflow


task_queue = "my-task-queue"
workflow_name = "SayHello"
activity_name = "say-hello-activity"


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(client, task_queue="encode-queue", workflows=[encodeflow], activities=[encode])
    result = await worker.run()

    
    print(result)
if __name__ == "__main__":
    asyncio.run(main())