import ccxt.async_support as ccxt
import asyncio
import yaml
import logging
from exchanges.exchanges import Exchange
from utils.scheduledtasks import periodic_task

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def loadSymbol(configPath='config/symbols.txt'):
    try:
        currency = []
        with open(configPath, 'r') as file:
            for line in file:
                currency.append(line.strip())
        return currency
    except Exception as e:
        logging.error(f"Failed to load symbol: {e}")
        raise

def loadConfig(configPath='config/config.yaml'):
    try:
        with open(configPath, 'r') as file:
            config = yaml.safe_load(file)
        required_keys = ['exchange', 'Zone', 'cronTasks', 'queryInterval','symbolsFilePath', 'defaultTimeframe', 'defaultThreshold', 'notificationChannels']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")

        return config
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        raise

def main():
    try:
        config = loadConfig()

        symbols = loadSymbol(config['symbolsFilePath'])
        if not symbols:
            logging.error("No symbols found in the specified file.")
            return
        
        if config['exchange'] == 'binance':
            exchange = Exchange(ccxt.binance(),config['defaultThreshold'])
        else:
            exchange = Exchange(ccxt.okx(),config['defaultThreshold'])

        asyncio.run(periodic_task(symbols, exchange, config, config['defaultTimeframe']))
        # if message:
        #     logging.info(f"Message to be sent:\n{message}")
        #     sendNotifications(message, config['notificationChannels'], config.get('telegram', {}), config.get('dingding', {}))
        # else:
        #     logging.info("No price changes exceed the threshold.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()
