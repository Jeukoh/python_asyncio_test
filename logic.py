import asyncio
import logging
import time
import functools
import sys


logger = logging.getLogger()

def _id_gen():
    id = 0
    while True:
        id += 1
        yield id

class Req:
    id_gen = _id_gen()
    def __init__(self) -> None:
        self.id = next(self.id_gen)
        
    @classmethod
    def init(cls):
        cls.id_gen = _id_gen()

def timechcker(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        id = args[0].id
        start = time.time()
        result = func(*args, **kwargs)
        logger.info('[%s] %s finish %s', id, func.__name__, time.time() - start)
        return result
    return wrapped
    
     
def async_timechecker(func):
    @functools.wraps(func)
    async def wrapped(*args):
        id = args[0].id
        start = time.time()
        logger.info('[%s] %s start at %s', id, func.__name__, start)
            # Some fancy foo stuff
        result = await func(*args)
        logger.info('[%s] %s finish %s', id, func.__name__, time.time() - start)
        return result
    return wrapped

@timechcker
def busy(request):
    i = 0
    for _ in range(1000000):
        i += _
    return request

@async_timechecker
async def async_busy(request):
    i = 0
    for _ in range(1000000):
        i += _
    return request

@timechcker
def io_job(request):
    time.sleep(2)
    return request

@async_timechecker
async def async_io_job(request):
    await asyncio.sleep(2)
    return request


if __name__ == '__main__':
    req1 = Req()
    req2 = Req()
    
    print(req1.id, req2.id)
    ret = busy(req1)
    ret = async_io_job(req2)
    x = asyncio.run(ret)
    print(x)