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
async def pull_msg(bulk_num=400):

    try:
        actions = []
        while 1:
            msg = lpop_redis("log-msg")
            _index = "test23-log-{0}".format(time.strftime("%Y%m%d"))
            _type = "test23-log"
            if msg:
                actions.append({
                    "_index": _index,
                    "_type": _type,
                    "_source": {
                        "msg": str(msg, encoding="utf-8"),
                    }
                })
                if actions.__len__() >= bulk_num:
                    await write_to_es(_index, actions)
                    actions.clear()
            else:
                print("not full", actions)
                break

    except Exception as e:
        log('error', str(e))


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(loop.run_until_complete(pull_msg()))



