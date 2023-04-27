import asyncio
import random
import string

from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow
import sys
sys.path.append('..')
# Import the activity and workflow from our other files
from  workflows.workflow6 import FindWorkflow2,search_database2


with workflow.unsafe.imports_passed_through():
    import random
    import string
    import redis

# task_queue = "my-task-queue"
# workflow_name = "SayHello"
# activity_name = "say-hello-activity"


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("192.168.120.129:7233")

    # Run the worker
    worker = Worker(
        client,
        task_queue="datasearchqueue",
        workflows=[FindWorkflow2],
        activities=[search_database2],
    )
    result = await worker.run()

    
    print(result)
if __name__ == "__main__":
    asyncio.run(main())