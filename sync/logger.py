# import logging

# def setup_logger():
#     logging.basicConfig(filename='sync.log', level=logging.INFO, format='%(asctime)s %(message)s')

# def log_sync(message):
#     logging.info(message)

# import datetime
# import logging

# logging.basicConfig(filename='sync.log', level=logging.INFO)

# def log_sync(message):
#     logging.info(f"{datetime.datetime.now()}: {message}")


import logging

# Configure logging with date and time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(message, *args):
    logging.info(message, *args)

def log_error(message, *args):
    logging.error(message, *args)
