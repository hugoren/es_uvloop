import asyncio
import uvloop
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from concurrent.futures import ThreadPoolExecutor
from blinker import signal
from utils import log
from utils import lpop_redis
# from utils import write_to_es

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)


es_signal = signal("es_signal")


@es_signal.connect
def write_to_es(actions):
    try:
        _index = "test23-log-{0}".format(time.strftime("%Y%m%d"))
        es = Elasticsearch(["192.168.6.23:9200"])
        bulk(es, actions, index=_index, raise_on_error=True)
    except Exception as e:
        print(e)
        log("error", str(e))


async def pull_msg(bulk_num=50):

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
                        "timestamp": datetime.now(),
                        "msg": str(msg, "utf-8"),
                    }
                })
                if actions.__len__() >= bulk_num:
                    # await write_to_es(_index, actions)
                    start_time = time.time()
                    es_signal.send(actions)
                    actions.clear()
                    print(time.time() - start_time)
            else:
                if actions:
                    # await write_to_es(_index, actions)
                    es_signal.send(actions)
                    actions.clear()

    except Exception as e:
        print(e)
        log('error', '写入es异常, 得有补偿机制, 异常原因:{0}'.format(str(e)))


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(loop.run_until_complete(pull_msg()))



