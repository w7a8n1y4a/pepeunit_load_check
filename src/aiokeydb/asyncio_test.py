import asyncio
import random
import time

from aiokeydb import KeyDBClient


keys = [str(item) for item in range(100)]


async def async_range(count):
    for i in range(count):
        yield(i)
        await asyncio.sleep(0.0)



async def redis_get_set(item, KeyDBClient):
    key = random.choice(keys)

    await KeyDBClient.async_wait_for_ready()

    await KeyDBClient.async_set(key, item)
    redis_topic_value = await KeyDBClient.async_get(key)

    await asyncio.sleep(1)

    return redis_topic_value

async def test():
    start = time.perf_counter()

    KeyDBClient.init_session(uri='redis://127.0.0.1:6379')
    for _ in range(10):
        results = await asyncio.gather(*(redis_get_set(item, KeyDBClient) for item in range(9998)))
        print(len(results))

    await KeyDBClient.aclose()
    print(f'avg_time: {(time.perf_counter() - start)/10}')

asyncio.run(test())



