import asyncio
import uvloop
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from utils import log
from utils import lpop_redis
from utils import write_to_es

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)


# 从队例拉取消息
async def pull_msg(bulk_num=100):

    try:
        actions = []
        while 1:
            start_time = time.time()
            msg = lpop_redis("log-msg")

            if msg:
                actions.append(str(msg, encoding="utf-8"))
                if actions.__len__() >= bulk_num:
                    print(actions)
                    # await write_to_es(str(msg, encoding="utf-8"))
                    # print(time.time() - start_time, msg)
                    print("full {}".format(bulk_num))
                    break
                    actions.clear()
                print(actions)
            else:
                print("not full", actions)
                actions.clear()

    except Exception as e:
        log('error', str(e))


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(loop.run_until_complete(pull_msg()))



