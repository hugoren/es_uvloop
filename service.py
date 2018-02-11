import asyncio
import uvloop
import time
import redis
import socketserver
from config import HOST, PORT
from utils import log
from utils import consumer_redis

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)


async def pull_msg():

    # r = await consumer_redis(loop)
    try:
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, max_connections=50)
        r = redis.Redis(connection_pool=pool)
        while 1:
            start_time = time.time()
            msg = r.lpop("log-msg")
        # msg = await consumer_redis(loop)
            print(time.time() - start_time, msg)

    except Exception as e:
        log('error', str(e))

if __name__ == "__main__":

    loop.run_until_complete(pull_msg())
    loop.run_forever()

