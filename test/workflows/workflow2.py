from datetime import timedelta
from temporalio import workflow

# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    from  activities.activitie1 import say_hello_activity
    

@workflow.defn
class say_hello_workflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            say_hello_activity, name, schedule_to_close_timeout=timedelta(seconds=5)
        )