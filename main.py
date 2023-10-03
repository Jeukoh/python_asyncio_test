from logic import (
    io_job,
    busy,
    async_busy,
    async_io_job,
    Req,
)
import asyncio
import logging
import sys
import time

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('async_test.log')]
)

logger = logging.getLogger()


"""
    1. 10 Request in queue
    busy + io_job + busy
"""

def situ_1():
    def my_program(req):
        busy(req)
        io_job(req)
        busy(req)
        
    reqs = [Req() for _ in range(10)]
    
    start = time.time()
    logger.info('start at %s', start)
    for req in reqs:
        my_program(req)
    logger.info('finish %s', time.time())
    logger.info('time_delta %s', time.time() - start)
    

"""
    2. 10 Request in queue
       busy + io_job + busy
       async wrapper
"""
async def situ_2():
    async def my_program(req):
        busy(req)
        io_job(req)
        busy(req)
    
    reqs = [Req() for _ in range(10)]
    
    start = time.time()
    logger.info('start at %s', start)
    ret = await asyncio.gather(*(my_program(req) for req in reqs))
    logger.info('finish %s', time.time())
    logger.info('time_delta %s', time.time() - start)
    print(ret)


"""
    3. 10 Request in queue
       busy + async_io_job + busy
       async wrapper
"""
async def situ_3():
    async def my_program(req):
        busy(req)
        await async_io_job(req)
        busy(req)
    
    reqs = [Req() for _ in range(10)]
    
    start = time.time()
    logger.info('start at %s', start)
    ret = await asyncio.gather(*(my_program(req) for req in reqs))
    logger.info('finish %s', time.time())
    logger.info('time_delta %s', time.time() - start)
    print(ret)
    
"""
    4. 10 Request in queue
       busy + async_io_job + busy
       async wrapper
"""
async def situ_4():
    async def my_program(req):
        await async_busy(req)
        await async_io_job(req)
        await async_busy(req)
    
    reqs = [Req() for _ in range(10)]
    
    start = time.time()
    logger.info('start at %s', start)
    ret = await asyncio.gather(*(my_program(req) for req in reqs))
    logger.info('finish %s', time.time())
    logger.info('time_delta %s', time.time() - start)
    print(ret)
    
"""
    5. 10 Request in queue
       async_busy + io_job + async_busy
       async wrapper
"""
async def situ_5():
    async def my_program(req):
        await async_busy(req)
        io_job(req)
        await async_busy(req)
    
    reqs = [Req() for _ in range(10)]
    
    start = time.time()
    logger.info('start at %s', start)
    ret = await asyncio.gather(*(my_program(req) for req in reqs))
    logger.info('finish %s', time.time())
    logger.info('time_delta %s', time.time() - start)
    print(ret)
    
if __name__ == '__main__':
    Req.init()
    situ_1()
    Req.init()
    asyncio.run(situ_2())
    Req.init()
    asyncio.run(situ_3())
    Req.init()
    asyncio.run(situ_4())
    Req.init()
    asyncio.run(situ_5())