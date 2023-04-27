import asyncio
import random
import string

from temporalio.client import Client
from temporalio.worker import Worker
import sys
sys.path.append('..')
# Import the activity and workflow from our other files
from  activities.activitie3 import returntrain
from  workflows.workflow4 import trainreturnflow


# task_queue = "my-task-queue"
# workflow_name = "SayHello"
# activity_name = "say-hello-activity"


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(client, task_queue="train-queue", workflows=[trainreturnflow], activities=[returntrain])
    result = await worker.run()

    
    print(result)
if __name__ == "__main__":
    asyncio.run(main())