import asyncio
from temporalio.client import Client

# Import the workflow from the previous code
from workflows.workflow2 import say_hello_workflow

task_queue = "say-hello-task-queue"
# workflow_name = say-hello-workflow
activity_name = "say-hello-activity"
workflow_id = "2222"
async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Execute a workflow
    result = await client.execute_workflow(say_hello_workflow.run, "Temporal", id=workflow_id, task_queue=task_queue)

    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())