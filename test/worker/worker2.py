import random
import string


from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
import sys
sys.path.append('..')
# Import the activity and workflow from our other files
from  activities.activitie1 import say_hello_activity
from  workflows.workflow2 import say_hello_workflow


task_queue = "say-hello-task-queue"
workflow_name = "say-hello-workflow"
activity_name = "say-hello-activity"


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(client, task_queue=task_queue, workflows=[say_hello_workflow],activities=[say_hello_activity])
    await worker.run()
    print("already")
    
   
if __name__ == "__main__":
    asyncio.run(main())