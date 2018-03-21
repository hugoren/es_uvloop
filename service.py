import time
import json
import uvloop
import asyncio

from blinker import signal
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from concurrent.futures import ThreadPoolExecutor

from utils import log
from utils import lpop_redis

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)


es_signal = signal("es_signal")


@es_signal.connect
def write_to_es(actions):
    try:
        _index = "log-{0}".format(time.strftime("%Y%m%d"))
        es = Elasticsearch(["192.168.6.23:9200"])
        bulk(es, actions, index=_index, raise_on_error=True)
    except Exception as e:
        print(e)
        log("error", str(e))


async def pull_msg(bulk_num=5):

    try:
        actions = []
        while 1:
            msg = lpop_redis("log-msg")
            if msg:
                actions.append(json.loads(msg))
                if len(actions) >= bulk_num:
                    es_signal.send(actions)
                    actions.clear()

    except Exception as e:
        print("pull_msg", e)
        log('error', '写入es异常, 得有补偿机制, 异常原因:{0}'.format(str(e)))


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(loop.run_until_complete(pull_msg()))



