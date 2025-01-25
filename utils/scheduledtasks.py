import asyncio
import logging
from datetime import datetime
from utils.parsetime import parseTimeframe, parseTime
from utils.log import Log
from notifications.dingding import sendDingDingMessage
from notifications.telegram import sendTelegramMessage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_result(symbol, exchange, times, num):
    await asyncio.sleep(0.2*num) # Prevent API access from being too frequent
    return await exchange.getResult(symbol, times['sinceCurrent'], times['sinceBefore'])

# Asynchronous query
async def main_async(symbols, exchange, config,times, timeFrame):
    try:
        tasks = [fetch_result(symbol, exchange, times, i) for i, symbol in enumerate(symbols)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        message = f'Price changes in the past {timeFrame}:'
        write = False
        for result in results:
            if isinstance(result, Exception):
                Log(f'{times['localTime']}  Task failed：{result}')
                logging.error(f"Task failed：{result}")
            else:
                if result:
                    write = True
                    message += result
        
        message += f'\n{times['localTime']}'
        
        if write:
            sendTelegramMessage(message, config['telegram']['token'], config['telegram']['chatId'])
            sendDingDingMessage(message, config['dingding']['webhook'], config['dingding']['secret'])
            Log(message+'\n')
        else:
            Log(f'{times['localTime']}  No price changes above threshold')

        print(message)
    finally:
        await exchange.exchange.close()

async def periodic_task(symbols, exchange, config, timeFrame):
    interval = parseTimeframe(config['queryInterval']) // 1000
    cronTasks = config['cronTasks']

    try:
        # When 'cronTasks' is 'false', it is executed in a loop, otherwise it is executed once and exits.
        while True:
            times = parseTime(config['Zone'],config['defaultTimeframe'])
            timeStart = datetime.now().timestamp()
            await main_async(symbols, exchange, config,times, timeFrame)
            timeEnd = datetime.now().timestamp()
            time = timeEnd - timeStart
            if cronTasks:
                break
            await asyncio.sleep(interval - time)  # 等待指定的间隔时间
    except:
        print('Task terminated') 
