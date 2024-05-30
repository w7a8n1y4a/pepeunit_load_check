import asyncio
import random
import time

from redis import asyncio as aioredis


keys = [str(item) for item in range(100)]


async def async_range(count):
    for i in range(count):
        yield(i)
        await asyncio.sleep(0.0)



async def redis_get_set(item, redis):
    key = random.choice(keys)

    await redis.set(key, item)
    redis_topic_value = await redis.get(key)

    await asyncio.sleep(1)

    return redis_topic_value

async def test():
    start = time.perf_counter()

    redis = await aioredis.from_url('redis://127.0.0.1:6379', encoding="utf-8", decode_responses=True)
    for _ in range(10):
        results = await asyncio.gather(*(redis_get_set(item, redis) for item in range(9998)))
        print(len(results))

    await redis.close()
    print(f'avg_time: {(time.perf_counter() - start)/10}')

asyncio.run(test())



