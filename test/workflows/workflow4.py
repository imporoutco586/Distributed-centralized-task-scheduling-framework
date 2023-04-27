from datetime import timedelta
from temporalio import workflow

# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    from  activities.activitie2 import trainmodel
    from  activities.activitie3 import returntrain
    from  activities.activitie3 import returntest

# @workflow.defn
# class trainflow:
#     @workflow.run
#     async def run(self, input):
#         return await workflow.execute_activity(
#             trainmodel, input, schedule_to_close_timeout=timedelta(seconds=5)
#         )

@workflow.defn 
class trainreturnflow:
    @workflow.run
    async def run(self):
        return await workflow.execute_activity(
            returntrain, schedule_to_close_timeout=timedelta(seconds=5)
        )

@workflow.defn 
class testreturnflow:
    @workflow.run
    async def run(self):
        return await workflow.execute_activity(
            returntest, schedule_to_close_timeout=timedelta(seconds=5)
        )
