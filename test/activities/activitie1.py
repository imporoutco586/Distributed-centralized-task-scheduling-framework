from temporalio import activity


@activity.defn
async def say_hello_activity(name: str) -> str:
    return f"Hello, {name}!"

@activity.defn
async def encode(input: str) -> str:
    return f"a encoded number is {24 * int(input) + 4}"

@activity.defn
async def decode(input:str) ->str:
    return f"a decoded number is {(int(input)-4)/24}"