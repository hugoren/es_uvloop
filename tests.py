import aioredis
import asyncio
import time

loop = asyncio.get_event_loop()


async def producer_redis(message):
    start_time = time.time()
    redis = await aioredis.create_redis_pool(
        'redis://127.0.0.1:6379', db=0, loop=loop)
    await redis.rpush('log-message', message)
    redis.close()
    await redis.wait_closed()
    print(time.time() - start_time)

while 1:
    loop.run_until_complete(producer_redis())
