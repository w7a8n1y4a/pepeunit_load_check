import asyncio
import time

from redis import asyncio as aioredis

async def async_range(count):
    for i in range(count):
        yield(i)
        await asyncio.sleep(0.0)


async def redis_get_set(item):
    redis = await aioredis.from_url('redis://127.0.0.1:6379', encoding="utf-8", decode_responses=True)
    await redis.set('123', item)                                                        
    redis_topic_value = await redis.get('123')

    await asyncio.sleep(1)
    
    await redis.aclose()

    return redis_topic_value

async def test():
    start = time.perf_counter()
    for _ in range(10): 
        results = await asyncio.gather(*(redis_get_set(item) for item in range(5000)))
        print(len(results)) 
    print(time.perf_counter() - start)

asyncio.run(test())



