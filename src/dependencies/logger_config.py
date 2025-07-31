import os
import logging
import sys

LOG_DIR = 'logs'

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'covid_fastapi_app.log')

if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
def get_logger(name: str = "app_logger") -> logging.Logger:
    """
    Get a logger with the specified name.
    If the logger already exists, it will return the existing logger.
    """
    return logging.getLogger(name)