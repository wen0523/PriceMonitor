import asyncio
import logging
import datetime
from parsetime import parseTimeframe

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_result(symbol, okx, times):
    return await okx.getResult(symbol, times['since'])

async def main_async(symbols, okx, times):
    try:
        tasks = [fetch_result(symbol, okx, times) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        message = '价格变动：'
        for result in results:
            if isinstance(result, Exception):
                logging.error(f"任务失败：{result}")
            else:
                message += result
        print(message)
    finally:
        await okx.exchange.close()

async def periodic_task(symbols, okx, times, timeFrame):
    interval = parseTimeframe(timeFrame) // 1000
    
    # 等待到指定开始时间
    if start_time:
        delay = (start_time - now).total_seconds()
        if delay > 0:
            print(f"等待 {delay} 秒，直到 {start_time}")
            await asyncio.sleep(delay)

    while True:
        asyncio.run(main_async(symbols, okx, times))
        await asyncio.sleep(interval)  # 等待指定的间隔时间
        
