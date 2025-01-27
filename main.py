import ccxt.async_support as ccxt
import asyncio
import yaml
import logging
from exchanges.exchanges import Exchange
from utils.scheduledtasks import periodic_task

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get currency
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

# Load configuration file
def loadConfig(configPath='config/config.yaml'):
    try:
        with open(configPath, 'r') as file:
            config = yaml.safe_load(file)
        required_keys = ['exchange', 'Zone', 'cronTasks', 'queryInterval','symbolsFilePath', 'defaultTimeframe', 'defaultThreshold', 'quantity', 'notificationChannels']
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
        
        # Determine exchange
        if config['exchange'] == 'binance':
            exchange = Exchange(ccxt.binance(),config['defaultThreshold'])
        else:
            exchange = Exchange(ccxt.okx(),config['defaultThreshold'])

        # Run program
        asyncio.run(periodic_task(symbols, exchange, config))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
     
if __name__ == "__main__":
    main()
