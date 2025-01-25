import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Record the log during the price inquiry process
def Log(message, logPath='log.txt'):
    try:
        with open(logPath, 'a') as file:
            file.write(message + '\n')
    except Exception as e:
        logging.error(f"Failed to write to {logPath}: {e}")
        raise