import asyncio
import random
import string
from temporalio.client import Client

# Import the workflow from the previous code
from workflows.workflow2 import say_hello_workflow
from workflows.workflow3 import encodeflow
from workflows.workflow3 import decodeflow
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
    result = await client.execute_workflow(say_hello_workflow.run, "Temporal", id=workflow_id, task_queue=task_queue)

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