import logging
import time
import aioredis
import redis
from functools import wraps
from sanic.response import json
from config import TOKEN
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from logging.handlers import RotatingFileHandler


def log(level, message):

    logger = logging.getLogger('es')

    #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        log_name = 'es.log'
        log_count = 2
        log_format = '%(asctime)s %(levelname)s %(module)s %(funcName)s-[%(lineno)d] %(message)s'
        log_level = logging.INFO
        max_bytes = 10 * 1024 * 1024
        handler = RotatingFileHandler(log_name, mode='a', maxBytes=max_bytes, backupCount=log_count)
        handler.setFormatter(logging.Formatter(log_format))
        logger.setLevel(log_level)
        logger.addHandler(handler)

    if level == 'info':
        logger.info(message)
    if level == 'error':
        logger.error(message)


def auth(token):
    def wrapper(func):
        @wraps(func)
        async def auth_token(req, *arg, **kwargs):
            try:
                value = req.headers.get(token)
                if value and TOKEN == value:
                    r = await func(req, *arg, **kwargs)
                    return json({'retcode': 0, 'stdout': r})
                else:
                    return json({'retcode': 1, 'stderr': 'status{}'.format(403)})
            except Exception as e:
                log('error', str(e))
                return json({'retcode': 1, 'stderr': str(e)})
        return auth_token
    return wrapper


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper


async def consumer_redis(loop):
    redis = await aioredis.create_redis_pool(
        'redis://127.0.0.1:6379', db=0, loop=loop, minsize=5, maxsize=50)
    r = await redis.lpop('log-msg')
    redis.close()
    await redis.wait_closed()
    return r


def rpush_redis(message):
    try:
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        r = redis.Redis(connection_pool=pool)
        r.rpush("log-msg", message)
    except Exception as e:
        log('error', str(e))


def lpop_redis(key):
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, max_connections=50)
    r = redis.Redis(connection_pool=pool)
    msg = r.lpop(key)
    return msg