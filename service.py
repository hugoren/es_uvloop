import asyncio
import uvloop
import time
from utils import log
from utils import lpop_redis

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)


async def pull_msg():

    try:
        while 1:
            start_time = time.time()
            msg = lpop_redis("log-msg")
            if msg:
                print(time.time() - start_time, msg)
    except Exception as e:
        log('error', str(e))


async def to_es(msg):
    pass

if __name__ == "__main__":
    loop.run_until_complete(pull_msg())
    loop.run_forever()

