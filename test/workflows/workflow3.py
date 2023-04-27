from datetime import timedelta
from temporalio import workflow

# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    from  activities.activitie1 import encode
    from  activities.activitie1 import decode
    

@workflow.defn
class encodeflow:
    @workflow.run
    async def run(self, input: str) -> str:
        return await workflow.execute_activity(
            encode, input, schedule_to_close_timeout=timedelta(seconds=5)
        )

@workflow.defn
class decodeflow:
    @workflow.run
    async def run(self, input: str) -> str:
        return await workflow.execute_activity(
            decode, input, schedule_to_close_timeout=timedelta(seconds=5)
        )